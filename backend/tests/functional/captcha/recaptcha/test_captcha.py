import pytest


class TestCaptcha:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.portal = portal
        self.url = "/document"

    def test_captcha_no_value(self, submit_form):
        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {"message": "Hello", "name": "John Doe"},
            },
            commit=True,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "No captcha token provided."

    def test_captcha_wrong_value(self, submit_form, mock_validation):
        mock_submit = mock_validation(response=False)
        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {"message": "Hello", "name": "John Doe"},
                "captcha": {"token": "12345"},
            },
            commit=True,
        )
        mock_submit.assert_called_once_with("12345", "private", "127.0.0.1")
        assert response.status_code == 400
        res = response.json()
        assert (
            "The code you entered was wrong, please enter the new one."
            in res["message"]
        )

    def test_captcha_correct_value(self, submit_form, mock_validation):
        mock_submit = mock_validation(response=True)
        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {"message": "Hello", "name": "John Doe"},
                "captcha": {"token": "12345"},
            },
            commit=True,
        )
        mock_submit.assert_called_once_with("12345", "private", "127.0.0.1")
        assert response.status_code == 200
