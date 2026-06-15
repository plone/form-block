from unittest.mock import Mock

import pytest


@pytest.fixture
def captcha(captcha_hcaptcha) -> dict:
    """Returns captcha settings for tests."""
    return captcha_hcaptcha


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
            "captcha": "hcaptcha",
        },
    }


@pytest.fixture
def mock_validation(monkeypatch):

    from plone.formblock.captcha import hcaptcha

    def func(response: bool = True):
        mock_submit = Mock(return_value=Mock(is_valid=response))
        monkeypatch.setattr(hcaptcha, "submit", mock_submit)
        return mock_submit

    return func
