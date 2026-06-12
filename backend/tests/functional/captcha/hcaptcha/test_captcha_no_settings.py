from copy import deepcopy

import pytest


@pytest.fixture
def captcha(captcha_hcaptcha) -> dict:
    """Returns captcha settings for tests."""
    value = deepcopy(captcha_hcaptcha)
    value["settings"]["private_key"] = ""
    return value


class TestCaptcha:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.portal = portal
        self.url = "/document"

    def test_captcha_no_settings(self, submit_form):
        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {"message": "Hello", "name": "John Doe"},
            },
            commit=True,
        )
        assert response.status_code == 500
        res = response.json()
        assert res["message"] == (
            "No hcaptcha private key configured. Go to path/to/site/@@hcaptcha-settings "
            "to configure."
        )
