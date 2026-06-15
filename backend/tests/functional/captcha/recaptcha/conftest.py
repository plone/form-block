from unittest.mock import Mock

import pytest


@pytest.fixture
def captcha(captcha_recaptcha) -> dict:
    """Returns captcha settings for tests."""
    return captcha_recaptcha


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
            "captcha": "recaptcha",
        },
    }


@pytest.fixture
def mock_validation(monkeypatch):

    from plone.formblock.captcha import recaptcha

    def func(response: bool = True):
        mock_submit = Mock(return_value=Mock(is_valid=response))
        monkeypatch.setattr(recaptcha, "submit", mock_submit)
        return mock_submit

    return func
