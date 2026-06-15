import pytest


@pytest.fixture(autouse=True)
def mock_event_handler(monkeypatch):
    monkeypatch.setenv("__TEST_EVENT_HANDLER", "1")


@pytest.fixture
def document_blocks() -> dict:
    return {
        "text-id": {"@type": "text"},
        "form-id": {
            "@type": "schemaForm",
            "subject": "block subject",
            "sender": "john@doe.com",
            "send": True,
            "schema": {
                "fieldsets": [
                    {
                        "id": "default",
                        "title": "Default",
                        "fields": ["message"],
                    },
                ],
                "properties": {
                    "message": {"title": "Message"},
                    "reply": {"title": "Reply"},
                },
                "required": [],
            },
        },
    }


class TestEvent:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal, get_messages):
        self.portal = portal
        self.get_messages = get_messages
        self.document_url = "/document"

    def test_trigger_event(self, submit_form, get_msg_body):
        response = submit_form(
            path="/document",
            data={
                "data": {"message": "just want to say hi"},
                "block_id": "form-id",
            },
            commit=True,
        )
        assert response.status_code == 200
        messages = self.get_messages()
        assert len(messages) == 1
        msg = messages[0]
        body_content = get_msg_body(msg)
        assert msg["To"] == "site_addr@plone.com"
        assert msg["To"] != "smith@doe.com"
        assert "Message  just want to say hi" in body_content
        assert "Reply  hello" in body_content
