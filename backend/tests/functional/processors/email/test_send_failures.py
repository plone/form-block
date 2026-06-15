import pytest


class TestEmailSendFailures:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.document_url = portal.document.absolute_url()
        self.url = "/document"

    def test_email_not_sent_if_block_id_is_not_given(self, submit_form):
        response = submit_form(
            path=self.url,
            data={},
            commit=True,
        )
        assert response.status_code == 400
        res = response.json()
        assert res["message"] == "Missing block_id"

    def test_email_not_sent_if_block_id_is_incorrect_or_not_present(self, submit_form):
        response = submit_form(
            path=self.url,
            data={
                "block_id": "unknown",
            },
            commit=True,
        )
        assert response.status_code == 400
        res = response.json()
        assert res["message"] == (
            f'Block with @type "schemaForm" and id "unknown" not found in this context: {self.document_url}'
        )

    def test_email_not_sent_if_block_id_is_correct_but_form_data_missing(
        self, submit_form
    ):
        response = submit_form(
            path=self.document_url,
            data={
                "block_id": "form-id",
            },
            commit=True,
        )
        assert response.status_code == 400
        res = response.json()
        assert res["message"] == "Empty form data."

    def test_email_not_sent_if_all_fields_are_not_in_form_schema(self, submit_form):
        response = submit_form(
            path=self.document_url,
            data={
                "block_id": "form-id",
                "data": {"xxx": "bar"},
            },
            commit=True,
        )
        res = response.json()
        assert response.status_code == 400
        assert res["message"] == "Empty form data."
