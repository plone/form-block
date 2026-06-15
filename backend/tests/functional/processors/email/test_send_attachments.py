import base64
import pytest


@pytest.fixture
def document_blocks() -> dict:
    return {
        "form-id": {
            "@type": "schemaForm",
            "send": True,
            "send_confirmation": True,
            "subject": "test subject",
            "confirmation_recipients": "${email}",
            "schema": {
                "fieldsets": [
                    {
                        "id": "default",
                        "title": "Default",
                        "fields": ["attachment", "name", "email"],
                    },
                ],
                "properties": {
                    "attachment": {"factory": "File Upload", "type": "object"},
                    "name": {"title": "Name"},
                    "email": {},
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

    def test_send_attachment(self, submit_form, file_content):
        response = submit_form(
            path=self.url,
            data={
                "data": {
                    "attachment": {
                        "data": base64.b64encode(file_content),
                        "filename": "test.pdf",
                    },
                },
                "block_id": "form-id",
            },
            commit=True,
        )
        assert response.status_code == 200
        messages = self.get_messages()
        assert len(messages) == 1
        msg = messages[0]
        assert 'Content-Disposition: attachment; filename="test.pdf"' in msg.as_string()

    def test_send_attachment_validate_size(
        self, monkeypatch, submit_form, file_content
    ):
        monkeypatch.setenv("FORM_ATTACHMENTS_LIMIT", "1")
        # increase file dimension
        file_content = file_content * 100
        response = submit_form(
            path=self.url,
            data={
                "data": {
                    "attachment": {
                        "data": base64.b64encode(file_content),
                        "filename": "test.pdf",
                    },
                },
                "block_id": "form-id",
            },
            commit=True,
        )
        assert response.status_code == 400
        assert (
            "Attachments too big. You uploaded 7.1 MB, but limit is 1 MB"
            in response.json()["message"]
        )
        assert len(self.get_messages()) == 0

    def test_send_confirmation(self, submit_form, get_msg_body):
        response = submit_form(
            path=self.url,
            data={
                "data": {
                    "message": "just want to say hi",
                    "name": "Smith",
                    "email": "smith@doe.com",
                },
                "block_id": "form-id",
            },
            commit=True,
        )
        assert response.status_code == 200
        messages = self.get_messages()
        assert len(messages) == 2
        # The first email is the one sent to the admins,
        # the second is the confirmation email sent to the user
        msg = messages[1]
        assert msg["From"] == "Plone test site <site_addr@plone.com>"
        assert msg["To"] == "smith@doe.com"
        assert msg["Subject"] == "test subject"
        body = get_msg_body(msg, "text/html")
        assert "Name</th><td>Smith</td>" in body
