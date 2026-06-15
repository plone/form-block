"""Unit tests for plone.formblock.utils.email.

These cover the two pure helpers used to build outgoing form e-mails:
``add_attachaments_to_msg`` and ``create_message``. They do not need a Plone
site, so they run as plain unit tests with fixtures and parametrization.
"""

from email import policy
from email.message import EmailMessage
from plone.formblock.utils.email import add_attachaments_to_msg
from plone.formblock.utils.email import create_message

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
