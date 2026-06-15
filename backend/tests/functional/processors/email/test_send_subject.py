import pytest


@pytest.fixture
def document_blocks() -> dict:
    return {
        "form-id": {
            "@type": "schemaForm",
            "send": True,
            "sender": "john@doe.com",
            "sender_name": "John Doe",
            "subject": "${message}",
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
        },
    }


class TestEmailSendSuccess:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal, get_messages):
        self.document_url = portal.document.absolute_url()
        self.url = "/document"
        self.get_messages = get_messages

    def test_email_sent_with_subject_from_form_data(self, submit_form):
        submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {"message": "Just to say hi", "name": "John Doe"},
            },
            commit=True,
        )
        msg = self.get_messages()[0]
        assert msg["Subject"] == "Just to say hi"
