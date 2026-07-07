"""Unit tests for plone.formblock.utils.email.

The pure helpers (``add_attachaments_to_msg``, ``create_message`` and
``substitute_variables``) need no Plone site and run as plain unit tests with
fixtures and parametrization. The helpers that read the registry or translate
strings (``is_mailhost_configured``, ``available_templates``,
``get_template_from_block``, ``format_property`` and ``addresses_from_block``)
need ``api`` access and live in :class:`TestApiSettings`.
"""

from copy import deepcopy
from email import policy
from email.message import EmailMessage
from plone import api
from plone.formblock.utils.email import add_attachaments_to_msg
from plone.formblock.utils.email import create_message
from plone.formblock.utils.email import substitute_variables

import base64
import pytest


@pytest.fixture
def message() -> EmailMessage:
    """A fresh message with a text body, ready to receive attachments."""
    msg = EmailMessage(policy=policy.SMTP)
    msg.set_content("plain text body")
    return msg


@pytest.fixture
def payload() -> bytes:
    """Raw attachment bytes, including non-text bytes."""
    return b"hello-bytes-\x00\x01\x02"


@pytest.fixture
def b64_attachment(payload):
    """Factory building a base64-encoded attachment dict (the form-upload shape)."""

    def factory(
        content_type: str = "application/octet-stream",
        filename: str = "file.bin",
    ) -> dict:
        return {
            "data": base64.b64encode(payload).decode("ascii"),
            "encoding": "base64",
            "content-type": content_type,
            "filename": filename,
        }

    return factory


class TestAddAttachmentsToMsg:
    def test_no_attachments(self, message):
        add_attachaments_to_msg(message, {})
        assert list(message.iter_attachments()) == []

    def test_base64_attachment_is_decoded(self, message, b64_attachment, payload):
        add_attachaments_to_msg(message, {"f": b64_attachment("image/png", "x.png")})
        attachments = list(message.iter_attachments())
        assert len(attachments) == 1
        att = attachments[0]
        assert att.get_filename() == "x.png"
        assert att.get_content_type() == "image/png"
        assert att.get_payload(decode=True) == payload

    @pytest.mark.parametrize(
        "content_type,filename",
        [
            ("image/png", "logo.png"),
            ("application/pdf", "report.pdf"),
            ("text/csv", "data.csv"),
        ],
    )
    def test_content_type_and_filename(
        self, message, b64_attachment, content_type, filename
    ):
        add_attachaments_to_msg(message, {"f": b64_attachment(content_type, filename)})
        att = next(iter(message.iter_attachments()))
        assert att.get_content_type() == content_type
        assert att.get_filename() == filename

    @pytest.mark.parametrize(
        "attachment",
        [
            {},
            {"data": ""},
            {"data": None},
            {"data": "", "content-type": "image/png", "filename": "x.png"},
        ],
        ids=["no-data-key", "empty-string", "none", "empty-with-metadata"],
    )
    def test_attachment_without_data_is_skipped(self, message, attachment):
        add_attachaments_to_msg(message, {"f": attachment})
        assert list(message.iter_attachments()) == []

    def test_default_content_type_when_missing(self, message):
        add_attachaments_to_msg(message, {"f": {"data": "plain", "filename": "a.bin"}})
        att = next(iter(message.iter_attachments()))
        assert att.get_content_type() == "application/octet-stream"
        assert att.get_payload(decode=True) == b"plain"

    def test_unencoded_str_data_is_utf8_encoded(self, message):
        add_attachaments_to_msg(message, {"f": {"data": "café"}})
        att = next(iter(message.iter_attachments()))
        assert att.get_payload(decode=True) == "café".encode()

    def test_multiple_attachments_skip_empty(self, message, b64_attachment):
        add_attachaments_to_msg(
            message,
            {
                "a": b64_attachment("image/png", "a.png"),
                "b": {"data": ""},
                "c": b64_attachment("text/plain", "c.txt"),
            },
        )
        attachments = list(message.iter_attachments())
        assert len(attachments) == 2
        assert {att.get_filename() for att in attachments} == {"a.png", "c.txt"}

    def test_bare_string_value_raises(self, message):
        # A bare string attachment value hits the default
        # ``application/octet-stream`` content type, which the stdlib email
        # package rejects for str payloads. This documents a latent bug: the
        # branch can never succeed as written.
        with pytest.raises(TypeError):
            add_attachaments_to_msg(message, {"f": "rawstring"})


class TestCreateMessage:
    def test_basic_headers(self):
        msg = create_message("from@x.com", "to@x.com", "Subject", "<b>hi</b>", "hi")
        assert msg["From"] == "from@x.com"
        assert msg["To"] == "to@x.com"
        assert msg["Subject"] == "Subject"

    def test_multipart_alternative_bodies(self):
        msg = create_message("from@x.com", "to@x.com", "S", "<b>hi</b>", "hi")
        assert msg.get_content_type() == "multipart/alternative"
        plain = msg.get_body(preferencelist=("plain",))
        html = msg.get_body(preferencelist=("html",))
        assert plain.get_content().strip() == "hi"
        assert html.get_content().strip() == "<b>hi</b>"

    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("a@x.com", "a@x.com"),
            ("a@x.com;b@x.com", "a@x.com, b@x.com"),
            ("a@x.com;b@x.com;c@x.com", "a@x.com, b@x.com, c@x.com"),
        ],
    )
    def test_to_semicolons_become_commas(self, raw, expected):
        msg = create_message("from@x.com", raw, "S", "<b>h</b>", "h")
        assert msg["To"] == expected

    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("c@x.com", "c@x.com"),
            ("c@x.com;d@x.com", "c@x.com, d@x.com"),
        ],
    )
    def test_bcc_semicolons_become_commas(self, raw, expected):
        msg = create_message("from@x.com", "to@x.com", "S", "<b>h</b>", "h", bcc=raw)
        assert msg["Bcc"] == expected

    def test_bcc_omitted_when_empty(self):
        msg = create_message("from@x.com", "to@x.com", "S", "<b>h</b>", "h")
        assert "Bcc" not in msg

    @pytest.mark.parametrize(
        "reply_to,expected",
        [
            ("r@x.com", "r@x.com"),
            ("", "from@x.com"),
        ],
        ids=["explicit", "defaults-to-from"],
    )
    def test_reply_to(self, reply_to, expected):
        msg = create_message(
            "from@x.com", "to@x.com", "S", "<b>h</b>", "h", reply_to=reply_to
        )
        assert msg["Reply-To"] == expected

    @pytest.mark.parametrize(
        "value,present",
        [
            ("bar", True),
            ("0", True),
            ("", False),
            (None, False),
        ],
        ids=["truthy", "zero-string", "empty-string", "none"],
    )
    def test_header_added_only_when_truthy(self, value, present):
        msg = create_message(
            "from@x.com", "to@x.com", "S", "<b>h</b>", "h", headers={"X-Test": value}
        )
        if present:
            assert msg["X-Test"] == value
        else:
            assert "X-Test" not in msg

    def test_multiple_headers(self):
        msg = create_message(
            "from@x.com",
            "to@x.com",
            "S",
            "<b>h</b>",
            "h",
            headers={"X-Foo": "bar", "X-Empty": "", "X-Num": "1"},
        )
        assert msg["X-Foo"] == "bar"
        assert msg["X-Num"] == "1"
        assert "X-Empty" not in msg

    def test_with_attachments(self, b64_attachment):
        msg = create_message(
            "from@x.com",
            "to@x.com",
            "S",
            "<b>h</b>",
            "h",
            attachments={"f": b64_attachment("image/png", "x.png")},
        )
        attachments = list(msg.iter_attachments())
        assert len(attachments) == 1
        assert attachments[0].get_filename() == "x.png"
        assert attachments[0].get_content_type() == "image/png"


class TestSubstituteVariables:
    """``substitute_variables`` is a pure ``${var}`` interpolation helper."""

    def test_no_variables_returns_unchanged(self):
        assert substitute_variables("plain text") == "plain text"

    @pytest.mark.parametrize(
        "template,context,expected",
        [
            ("hi ${name}", {"name": "Bob"}, "hi Bob"),
            ("${a}-${b}", {"a": "1", "b": "2"}, "1-2"),
            ("${g}, ${name}!", {"g": "Hello", "name": "Ana"}, "Hello, Ana!"),
        ],
    )
    def test_substitution_with_context(self, template, context, expected):
        assert substitute_variables(template, context=context) == expected

    def test_missing_variable_becomes_empty(self):
        assert substitute_variables("a${x}b", context={}) == "ab"

    def test_form_data_used_when_context_is_none(self):
        assert substitute_variables("hi ${name}", form_data={"name": "X"}) == "hi X"

    def test_context_takes_precedence_over_form_data(self):
        # When both are given, ``form_data`` is ignored entirely.
        result = substitute_variables(
            "${a}", context={"a": "ctx"}, form_data={"a": "fd"}
        )
        assert result == "ctx"

    def test_both_none_treats_all_variables_as_missing(self):
        assert substitute_variables("x${y}z") == "xz"

    def test_non_string_substitution_value_raises(self):
        # ``re.sub`` requires the replacement to be a string, so a non-string
        # value in the context surfaces as a TypeError. Documents a latent
        # constraint: callers must pass stringified values.
        with pytest.raises(TypeError):
            substitute_variables("${n}", context={"n": 5})


class TestApiSettings:
    @pytest.fixture(autouse=True)
    def _setup(self, portal_class):
        self.portal = portal_class

    def test_is_mailhost_configured(self):
        from plone.formblock.utils.email import is_mailhost_configured

        assert is_mailhost_configured() is True

    def test_available_templates(self):
        from plone.formblock.utils.email import available_templates

        templates = available_templates()
        assert isinstance(templates, dict)
        assert "default" in templates
        assert isinstance(templates["default"], str)

    def test_get_template_from_block_defaults_to_default_template(self):
        from plone.formblock.interfaces import DEFAULT_TEMPLATE
        from plone.formblock.utils.email import get_template_from_block

        # No ``mail_template`` key -> resolves the "default" entry.
        assert get_template_from_block({}) == DEFAULT_TEMPLATE

    def test_get_template_from_block_unknown_name_falls_back(self):
        from plone.formblock.interfaces import DEFAULT_TEMPLATE
        from plone.formblock.utils.email import get_template_from_block

        block = {"mail_template": "does-not-exist"}
        assert get_template_from_block(block) == DEFAULT_TEMPLATE

    def test_get_template_from_block_returns_selected_template(self):
        from plone.formblock.utils.email import get_template_from_block

        record = "schemaform.mail_templates_json"
        original = api.portal.get_registry_record(record)
        try:
            api.portal.set_registry_record(
                record, {**original, "custom": "CUSTOM BODY"}
            )
            block = {"mail_template": "custom"}
            assert get_template_from_block(block) == "CUSTOM BODY"
        finally:
            api.portal.set_registry_record(record, original)

    @pytest.mark.parametrize(
        "factory,value,expected",
        [
            ("label_boolean_field", True, "Yes"),
            ("label_boolean_field", False, "No"),
            ("termsAccepted", True, "Yes"),
            ("termsAccepted", False, "No"),
            # Identity check: only ``True`` is "Yes"; a truthy non-True is "No".
            ("label_boolean_field", "true", "No"),
        ],
    )
    def test_format_property_boolean(self, factory, value, expected):
        from plone.formblock.utils.email import format_property

        assert format_property(factory, value) == expected

    def test_format_property_checkbox_group_joins_list(self):
        from plone.formblock.utils.email import format_property

        assert format_property("checkbox_group", ["a", "b", "c"]) == "a<br/>b<br/>c"

    def test_format_property_checkbox_group_non_list_is_stringified(self):
        from plone.formblock.utils.email import format_property

        # Only list values are joined; anything else falls through to ``str``.
        assert format_property("checkbox_group", "single") == "single"

    @pytest.mark.parametrize("factory", ["label_date_field", "label_datetime_field"])
    def test_format_property_dates_are_localized(self, factory):
        from plone.formblock.utils.email import format_property

        result = format_property(factory, "2026-07-06")
        assert "2026" in result

    @pytest.mark.parametrize(
        "value,expected",
        [(42, "42"), ("plain", "plain"), (None, "None")],
    )
    def test_format_property_default_stringifies(self, value, expected):
        from plone.formblock.utils.email import format_property

        assert format_property("text", value) == expected

    def test_addresses_from_block_defaults(self):
        from plone.formblock.utils.email import addresses_from_block

        addresses = addresses_from_block({}, {})
        assert addresses.sender == "Plone test site <site_addr@plone.com>"
        assert addresses.admin_recipients == "site_addr@plone.com"
        assert addresses.bcc == ""
        assert addresses.confirmation_recipients == ""

    def test_addresses_from_block_explicit_values(self):
        from plone.formblock.utils.email import addresses_from_block

        block = {
            "sender": "me@x.com",
            "sender_name": "Me",
            "recipients": "admin@x.com",
            "bcc": "b@x.com",
            "confirmation_recipients": "c@x.com",
        }
        addresses = addresses_from_block(block, {})
        assert addresses.sender == "Me <me@x.com>"
        assert addresses.admin_recipients == "admin@x.com"
        assert addresses.bcc == "b@x.com"
        assert addresses.confirmation_recipients == "c@x.com"

    def test_addresses_from_block_substitutes_variables(self):
        from plone.formblock.utils.email import addresses_from_block

        block = {"sender": "${email}", "confirmation_recipients": "${email}"}
        form_data = {"email": "user@x.com"}
        addresses = addresses_from_block(block, form_data)
        # sender_name falls back to the site default; the address is substituted.
        assert addresses.sender == "Plone test site <user@x.com>"
        assert addresses.confirmation_recipients == "user@x.com"

    def test_addresses_from_block_empty_recipients_not_defaulted(self):
        from plone.formblock.utils.email import addresses_from_block

        # ``recipients`` defaults to the site address only when the key is
        # absent; an explicit empty string is preserved as-is.
        addresses = addresses_from_block({"recipients": ""}, {})
        assert addresses.admin_recipients == ""


class TestRequestHeadersFromBlock:
    @pytest.fixture(autouse=True)
    def _setup(self, functional_portal, functional_http_request):
        from plone.formblock.utils.email import request_headers_from_block

        self.portal = functional_portal
        self.request = functional_http_request
        self.func = request_headers_from_block

    @pytest.mark.parametrize(
        "httpHeaders,headers,total",
        (
            ("", {"HTTP_USER_AGENT": "Mozilla/5.0"}, 0),
            ("USER_AGENT", {"HTTP_USER_AGENT": "Mozilla/5.0"}, 1),
            ("REMOTE_ADDR", {"HTTP_USER_AGENT": "Mozilla/5.0"}, 0),
            (
                "X_FORWARDED_FOR\nREMOTE_ADDR\nUSER_AGENT",
                {"HTTP_USER_AGENT": "Mozilla/5.0"},
                1,
            ),
            (
                "X_FORWARDED_FOR\nREMOTE_ADDR\nUSER_AGENT",
                {"HTTP_USER_AGENT": "Mozilla/5.0", "REMOTE_ADDR": "200.162.135.12"},
                2,
            ),
        ),
    )
    def test_request_headers_from_block_empty(
        self, block_info, httpHeaders: str, headers: dict[str, str], total: int
    ):
        # Set values in the block
        block = deepcopy(block_info)
        block["httpHeaders"] = httpHeaders
        # Set headers in request
        request = self.request
        for key, value in headers.items():
            request.environ[key] = value
        headers = self.func(block, request)
        assert len(headers) == total
