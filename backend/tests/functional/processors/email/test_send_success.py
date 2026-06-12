import pytest


class TestEmailSendSuccess:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal, get_messages):
        self.document_url = portal.document.absolute_url()
        self.url = "/document"
        self.get_messages = get_messages

    def test_email_sent_with_fallback_subject_and_sender(self, submit_form):
        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {"message": "Hello", "name": "John Doe"},
            },
            commit=True,
        )
        assert response.status_code == 200
        res = response.json()

        assert res["data"] == {"message": "Hello", "name": "John Doe"}

        messages = self.get_messages()
        assert len(messages) == 1
        msg = messages[0]
        assert msg["Subject"] == "Form Submission"
        assert msg["From"] == "Plone test site <site_addr@plone.com>"
        assert msg["To"] == "site_addr@plone.com"
        assert msg["Reply-To"] == "Plone test site <site_addr@plone.com>"

    def test_email_sent_filter_data(self, submit_form, get_msg_body):
        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {"message": "Hello", "name": "John Doe", "color": "black"},
            },
            commit=True,
        )
        res = response.json()
        assert response.status_code == 200
        assert res["data"] == {"message": "Hello", "name": "John Doe"}

        messages = self.get_messages()
        assert len(messages) == 1
        msg = messages[0]
        body = get_msg_body(msg)
        assert msg["Subject"] == "Form Submission"
        assert msg["From"] == "Plone test site <site_addr@plone.com>"
        assert msg["To"] == "site_addr@plone.com"
        assert msg["Reply-To"] == "Plone test site <site_addr@plone.com>"
        assert "Message  Hello" in body
        assert "Name  John Doe" in body
        assert "Color  black" not in body

    def test_email_sent_html(self, submit_form, get_msg_body):
        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
                "data": {"message": "Hello", "name": "John Doe"},
            },
            commit=True,
        )
        res = response.json()
        assert response.status_code == 200
        assert res["data"] == {"message": "Hello", "name": "John Doe"}

        messages = self.get_messages()
        assert len(messages) == 1
        msg = messages[0]
        body = get_msg_body(msg, "text/html")
        assert msg["Subject"] == "Form Submission"
        assert msg["From"] == "Plone test site <site_addr@plone.com>"
        assert msg["To"] == "site_addr@plone.com"
        assert msg["Reply-To"] == "Plone test site <site_addr@plone.com>"
        assert "Message</th><td>Hello</td>" in body
        assert "Name</th><td>John Doe</td>" in body
