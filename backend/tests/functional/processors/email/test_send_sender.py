import pytest


@pytest.fixture
def document_blocks() -> dict:
    return {
        "form-id": {
            "@type": "schemaForm",
            "send": True,
            "sender": "${email}",
            "sender_name": "${name}",
            "bcc": "${bcc}",
            "subject": "${message}",
            "schema": {
                "fieldsets": [
                    {
                        "id": "default",
                        "title": "Default",
                        "fields": ["message", "name", "email", "bcc"],
                    },
                ],
                "properties": {
                    "message": {"title": "Message"},
                    "email": {"title": "Email"},
                    "name": {"title": "Name"},
                    "bcc": {"title": "Bcc"},
                },
                "required": [],
            },
        },
    }


class TestEmailSendSuccess:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal, get_messages, get_messages_rcpt):
        self.document_url = portal.document.absolute_url()
        self.url = "/document"
        self.get_messages = get_messages
        self.get_messages_rcpt = get_messages_rcpt

    def test_email_with_sender_from_form_data(self, submit_form):
        submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {
                    "message": "Just to say hi",
                    "name": "Smith",
                    "email": "smith@doe.com",
                    "bcc": "foo@doe.com",
                },
            },
            commit=True,
        )
        messages = self.get_messages()
        msg = messages[0]
        assert msg["Reply-To"] == "Smith <smith@doe.com>"
        # BCC will not be in the email headers, but MockMailHost stores
        # all the recipients in a separate attribute, so we can check it there.
        rcpt = self.get_messages_rcpt()[0]
        assert "foo@doe.com" in rcpt
