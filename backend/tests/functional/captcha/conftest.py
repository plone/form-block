import pytest


@pytest.fixture
def block_data(manager_request):
    def func(path="/document", block_id="form-id"):
        response = manager_request.get(path)
        return response.json()["blocks"][block_id]

    return func


@pytest.fixture
def block_schema(block_data):
    def func(path="/document", block_id="form-id"):
        data = block_data(path, block_id)
        return data["schema"]

    return func


@pytest.fixture
def captcha_payload(block_schema):
    """Returns a valid payload for the norobots captcha."""

    def func(path="/document", block_id="form-id") -> dict:
        schema = block_schema(path, block_id)
        captcha_props = schema["properties"]["captchaWidget"]["captcha_props"]
        return {"provider": "norobots-captcha", "props": captcha_props}

    return func
