from plone import api

import email
import pytest
import transaction


@pytest.fixture
def submit_form(manager_request):
    def func(path: str, data: dict, commit: bool = False):
        path = f"{path}/@schemaform-data"
        response = manager_request.post(
            path,
            json=data,
        )
        if commit:
            transaction.commit()
        return response

    return func


@pytest.fixture()
def http_request(functional):
    return functional["request"]


@pytest.fixture(scope="session")
def get_messages():
    from email import policy
    from email.message import Message

    default_policy = policy.default

    def func() -> list[Message]:
        mailhost = api.portal.get_tool("MailHost")
        messages = []
        for msg in mailhost.messages:
            message = email.message_from_bytes(msg, policy=default_policy)
            messages.append(message)
        return messages

    return func


@pytest.fixture(scope="session")
def get_messages_rcpt():

    def func() -> list[tuple[str, ...]]:
        mailhost = api.portal.get_tool("MailHost")
        return mailhost.messages_to

    return func


@pytest.fixture(scope="session")
def get_msg_body():
    from email.message import Message

    def func(msg: Message, content_type: str = "text/plain") -> str:
        return str(
            next(
                p.get_payload()
                for p in msg.walk()
                if p.get_content_type() == content_type
            )
        )

    return func


@pytest.fixture
def captcha_hcaptcha() -> dict:
    """Returns hCaptcha settings for tests."""
    from plone.formwidget.hcaptcha.interfaces import IHCaptchaSettings

    return {
        "type": "hcaptcha",
        "iface": IHCaptchaSettings,
        "settings": {
            "public_key": "public",
            "private_key": "private",
        },
    }


@pytest.fixture
def captcha_norobots() -> dict:
    """Returns norobots settings for tests."""
    from collective.z3cform.norobots.browser.interfaces import INorobotsWidgetSettings

    return {
        "type": "norobots-captcha",
        "iface": INorobotsWidgetSettings,
        "settings": {"questions": ("What is 4 + 4 ?::8",)},
    }


@pytest.fixture
def captcha_recaptcha() -> dict:
    """Returns hCaptcha settings for tests."""
    from plone.formwidget.recaptcha.interfaces import IReCaptchaSettings

    return {
        "type": "recaptcha",
        "iface": IReCaptchaSettings,
        "settings": {
            "public_key": "public",
            "private_key": "private",
        },
    }


@pytest.fixture
def captcha() -> dict:
    """Returns captcha settings for tests."""
    return {}


@pytest.fixture
def document_blocks(captcha) -> dict:
    blocks: dict[str, dict] = {
        "text-id": {"@type": "text"},
        "form-id": {
            "@type": "schemaForm",
            "subject": "block subject",
            "default_from": "foo@foo.com",
            "default_name": "John Doe",
            "sender": "noreply@plone.org",
            "sender_name": "Plone",
            "send": False,
            "store": True,
            "thankyou": "${formfields}",
            "schema": {
                "fieldsets": [
                    {
                        "id": "default",
                        "title": "Default",
                        "fields": ["message"],
                    },
                ],
                "properties": {
                    "message": {"title": "Message"},
                    "name": {"title": "Name"},
                    "reply": {"title": "Reply"},
                },
                "required": [],
            },
        },
    }
    if captcha_type := captcha.get("type"):
        blocks["form-id"]["captcha"] = captcha_type
    return blocks


@pytest.fixture
def payload_document(document_blocks) -> dict:
    layout = list(document_blocks.keys())
    return {
        "type": "Document",
        "id": "document",
        "title": "Document",
        "blocks": document_blocks,
        "blocks_layout": {"items": layout},
    }


@pytest.fixture
def create_document():
    def func(portal, payload):
        with api.env.adopt_roles(["Manager"]):
            document = api.content.create(
                container=portal,
                **payload,
            )
            api.content.transition(obj=document, transition="publish")
        return document

    return func


@pytest.fixture
def configure_captcha_adapter():
    def func(captcha: dict):
        registry = api.portal.get_tool("portal_registry")
        registry.registerInterface(captcha["iface"])
        settings = registry.forInterface(captcha["iface"])
        for key, value in captcha["settings"].items():
            setattr(settings, key, value)
        return settings

    return func


@pytest.fixture
def captcha_settings(captcha, configure_captcha_adapter):
    def func():
        if not captcha:
            # No captcha settings needed for tests
            return
        return configure_captcha_adapter(captcha)

    return func


@pytest.fixture
def portal(functional_portal, captcha_settings, payload_document, create_document):
    # Create a document with the form block
    create_document(functional_portal, payload_document)
    # Set captcha settings if needed
    captcha_settings()
    # commit settings
    transaction.commit()

    return functional_portal
