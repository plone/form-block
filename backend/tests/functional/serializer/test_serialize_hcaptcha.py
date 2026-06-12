import pytest


@pytest.fixture
def captcha(captcha_hcaptcha) -> dict:
    """Returns captcha settings for tests."""
    return captcha_hcaptcha


class TestBlockSerialization:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.url = "/document"

    def test_serializer_with_hcaptcha(self, anon_request):
        response = anon_request.get(self.url)
        res = response.json()
        captcha_props = res["blocks"]["form-id"]["captcha_props"]
        assert captcha_props == {"provider": "hcaptcha", "public_key": "public"}
