import pytest


class TestCaptcha:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.portal = portal
        self.url = "/document"

    def test_captcha_field_is_present(self, block_schema):
        schema = block_schema()
        assert "captchaWidget" in schema["properties"]
        field = schema["properties"]["captchaWidget"]
        assert field["captcha_props"]["provider"] == "protected_1"

    def test_captcha_no_value(self, submit_form):
        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {"message": "Hello", "name": "John Doe"},
            },
            commit=True,
        )
        assert response.status_code == 200

    def test_captcha_wrong_value(self, submit_form):
        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {
                    "message": "Hello",
                    "name": "John Doe",
                    "protected_1": "should be empty",
                },
            },
            commit=True,
        )
        assert response.status_code == 400
        res = response.json()
        assert "Error submitting form." in res["message"]

    def test_captcha_empty_value(self, submit_form):
        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {"message": "Hello", "name": "John Doe", "protected_1": ""},
            },
            commit=True,
        )
        assert response.status_code == 400
