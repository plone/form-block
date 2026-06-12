import pytest


@pytest.fixture
def captcha(captcha_norobots) -> dict:
    """Returns norobots settings for tests."""
    return captcha_norobots


@pytest.fixture
def document_blocks() -> dict:
    return {
        "form-id": {
            "@type": "schemaForm",
            "send": True,
            "store": False,
            "schema": {
                "fieldsets": [
                    {
                        "id": "default",
                        "title": "Default",
                        "fields": ["message", "name"],
                    },
                ],
                "properties": {
                    "message": {"title": "Message"},
                    "name": {"title": "Name"},
                },
                "required": [],
            },
            "captcha": "norobots-captcha",
        },
    }
