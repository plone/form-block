import pytest


@pytest.fixture
def captcha(captcha_recaptcha) -> dict:
    """Returns captcha settings for tests."""
    return captcha_recaptcha


class TestBlockSerializationRecaptcha:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.url = "/document"

    def test_serializer_with_recaptcha(self, anon_request):
        response = anon_request.get(self.url)
        res = response.json()
        captcha_props = res["blocks"]["form-id"]["captcha_props"]
        assert captcha_props == {
            "provider": "recaptcha",
            "public_key": "public",
            "use_recaptcha_net": True,
        }
