from collections.abc import Sequence

import pytest


@pytest.fixture
def configure_captcha_adapters(
    configure_captcha_adapter, captcha_hcaptcha, captcha_norobots, captcha_recaptcha
):
    """Configure all captcha adapters for tests."""
    import transaction

    adapters = [captcha_hcaptcha, captcha_norobots, captcha_recaptcha]
    settings = {adapter["type"]: adapter for adapter in adapters}

    def func(adapters: Sequence[str] = ("hcaptcha", "norobots", "recaptcha")):
        for adapter in adapters:
            info = settings[adapter]
            configure_captcha_adapter(info)

        transaction.commit()
        return None

    return func


class TestCaptchaVocabulary:
    endpoint: str = "/@vocabularies/plone.formblock.captcha.providers"

    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.portal = portal

    def test_no_adapters(self, manager_request):
        response = manager_request.get(self.endpoint)
        assert response.status_code == 200
        data = response.json()
        # no adapters configured
        assert data["@id"].endswith(self.endpoint)

        assert data["items_total"] == 2
        assert data["items"][0] == {
            "title": "NoRobots ReCaptcha Support",
            "token": "norobots-captcha",
        }
        assert data["items"][1] == {"title": "Honeypot Support", "token": "honeypot"}

    @pytest.mark.parametrize(
        "token,title",
        [
            ["recaptcha", "Google ReCaptcha"],
            ["hcaptcha", "HCaptcha"],
            ["norobots-captcha", "NoRobots ReCaptcha Support"],
        ],
    )
    def test_adapters(self, manager_request, configure_captcha_adapters, token, title):
        configure_captcha_adapters(adapters=[token])
        response = manager_request.get(self.endpoint)
        assert response.status_code == 200
        data = response.json()
        filtered_items = [item for item in data["items"] if item["token"] == token]
        assert filtered_items == [{"title": title, "token": token}]
