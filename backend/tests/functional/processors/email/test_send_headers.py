import pytest


@pytest.fixture
def document_blocks() -> dict:
    return {
        "form-id": {
            "@type": "schemaForm",
            "send": True,
            "sender": "john@doe.com",
            "sender_name": "John Doe",
            "subject": "test subject",
            "httpHeaders": [
                "REMOTE_ADDR",
                "PATH_INFO",
            ],
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

    def test_email_with_headers(self, submit_form):
        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {"message": "Hello", "name": "John Doe"},
            },
            commit=True,
        )
        assert response.status_code == 200

        msg = self.get_messages()[0]
        assert "REMOTE_ADDR" in msg
        assert "PATH_INFO" in msg
