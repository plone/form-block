from plone.formblock.interfaces import SchemaFormBlock

import pytest


@pytest.fixture
def block_info() -> SchemaFormBlock:
    return {
        "@type": "schemaForm",
        "admin_info": "Foo bar",
        "cancel_label": "Cancel",
        "captcha": "honeypot",
        "captcha_props": {"provider": "protected_1"},
        "data_wipe": -1,
        "httpHeaders": "X_FORWARDED_FOR\nREMOTE_ADDR\nUSER_AGENT",
        "recipients": "foo@bar.edu",
        "schema": {
            "fieldsets": [
                {
                    "fields": [
                        "name",
                        "email",
                        "interests",
                        "message",
                        "captchaWidget",
                    ],
                    "id": "default",
                    "title": "Default",
                }
            ],
            "properties": {
                "captchaToken": {},
                "captchaWidget": {
                    "captcha_props": {"provider": "protected_1"},
                    "title": "honeypot",
                    "widget": "honeypot",
                },
                "email": {
                    "description": "Your e-mail",
                    "factory": "label_email",
                    "id": "email",
                    "title": "E-mail",
                    "type": "string",
                    "widget": "email",
                },
                "interests": {
                    "choices": [
                        ["Plone", "Plone"],
                        ["Python", "Python"],
                        ["React", "React"],
                        ["Star Trek", "Star Trek"],
                        ["World Cup", "World Cup"],
                    ],
                    "description": "Select some topics you want to know more",
                    "factory": "checkbox_group",
                    "id": "interests",
                    "title": "Your Interests",
                    "type": "array",
                    "values": ["Plone", "Python", "React", "Star Trek", "World Cup"],
                    "widget": "checkbox_group",
                },
                "message": {
                    "description": "Please, let us know a bit more about you",
                    "factory": "textarea",
                    "id": "message",
                    "minLength": "50",
                    "title": "Additional information",
                    "type": "string",
                    "widget": "textarea",
                },
                "name": {
                    "description": "Please, tell us your name",
                    "factory": {"label": "Text", "value": "label_text_field"},
                    "id": "name",
                    "placeholder": "John Smith",
                    "title": "Your name",
                    "type": "string",
                },
            },
            "required": ["name", "email", "interests", "message"],
        },
        "send": True,
        "sender": "noreply@plone.org",
        "sender_name": "Plone",
        "show_cancel": True,
        "store": True,
        "subject": "Plone Form Block",
        "submit_label": "Submit",
        "success": "Thank you! You have submitted the following data:",
        "thankyou": "${formfields}",
        "title": "Contact our Team",
    }
