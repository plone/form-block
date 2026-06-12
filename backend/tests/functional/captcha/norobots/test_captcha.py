import pytest


class TestCaptcha:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.portal = portal
        self.url = "/document"

    def test_installed(self, block_schema):
        schema = block_schema(self.url)
        assert "captchaWidget" in schema["properties"]
        widget = schema["properties"]["captchaWidget"]
        assert "id" in widget["captcha_props"]
        assert "id_check" in widget["captcha_props"]
        assert "title" in widget["captcha_props"]

    def test_installed_but_field_not_in_form(self, submit_form):
        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {
                    "message": "Hello",
                    "name": "John Doe",
                },
            },
            commit=True,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "No captcha token provided."

    def test_field_in_form_pass_validation(self, submit_form, captcha_payload):
        data = {
            "block_id": "form-id",
            "data": {
                "message": "Hello",
                "name": "John Doe",
                "captchaWidget": "8",
            },
            "captcha": captcha_payload(),
        }
        response = submit_form(
            path=self.url,
            data=data,
            commit=True,
        )
        assert response.status_code == 200

    def test_field_in_form_compiled_fail_validation(self, submit_form, captcha_payload):
        data = {
            "block_id": "form-id",
            "data": {
                "message": "Hello",
                "name": "John Doe",
                "captchaWidget": "5",
            },
            "captcha": captcha_payload(),
        }
        response = submit_form(
            path=self.url,
            data=data,
            commit=True,
        )
        assert response.status_code == 400
        assert (
            response.json()["message"]
            == "The code you entered was wrong, please enter the new one."
        )
