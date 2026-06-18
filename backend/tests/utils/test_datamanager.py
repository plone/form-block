from plone.formblock.utils import datamanager
from souper.soup import Record

import pytest


DOCUMENT_DATA = {
    "type": "Document",
    "id": "doc",
    "title": "Contact Form",
    "blocks": {
        "text-id": {"@type": "text"},
        "form-id": {
            "@type": "schemaForm",
            "subject": "block subject",
            "default_from": "foo@foo.com",
            "default_name": "John Doe",
            "sender": "noreply@plone.org",
            "sender_name": "Plone",
            "send": False,
            "store": True,
            "thankyou": "${formfields}",
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
                    "name": {"title": "Name"},
                    "reply": {"title": "Reply"},
                },
                "required": [],
            },
        },
    },
    "blocks_layout": {
        "items": ["text-id", "form-id"],
    },
}

RECORDS = [
    [
        {
            "field_id": "message",
            "value": "Hello, this is a message.",
        },
        {
            "field_id": "name",
            "value": "John Doe",
        },
        {
            "field_id": "reply",
            "value": "foo@bar.com",
        },
    ],
    [
        {
            "field_id": "message",
            "value": "Hola.",
        },
        {
            "field_id": "name",
            "value": "Juan Doe",
        },
        {
            "field_id": "reply",
            "value": "bar@foo.com",
        },
    ],
]


@pytest.fixture
def block():
    return DOCUMENT_DATA["blocks"]["form-id"]


@pytest.fixture
def populate_data_store(form_data_store_factory):
    def func(document, block_id):
        data_store = form_data_store_factory(context=document, block_id=block_id)
        for record in RECORDS:
            data_store.add(record)

    return func


@pytest.mark.portal(
    content=[DOCUMENT_DATA],
)
class TestRecords:
    block_id = "form-id"

    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.portal = portal
        self.document = portal.doc

    def test_total_records_in_block_empty(self):
        """Test total_records_in_block utility function."""
        total = datamanager.total_records_in_block(self.document, self.block_id)
        assert total == 0

    def test_total_records(self, populate_data_store):
        """Test total_records_in_block utility function."""
        # Adds 2 records to the data store
        populate_data_store(self.document, self.block_id)
        total = datamanager.total_records_in_block(self.document, self.block_id)
        assert total == 2


def test_get_schema_fields_from_block(block):
    fields = datamanager.get_schema_fields_from_block(block)
    assert fields == [
        {"field_id": "message", "label": "Message"},
        {"field_id": "name", "label": "Name"},
        {"field_id": "reply", "label": "Reply"},
    ]


@pytest.mark.parametrize("form_data", RECORDS)
def test_record_from_form_data(block, form_data):
    fields = datamanager.get_schema_fields_from_block(block)
    record = datamanager.record_from_form_data(
        form_data, block_id="form-id", form_fields=fields
    )
    assert record is not None
    assert isinstance(record, Record)
    assert record.attrs["message"] == form_data[0]["value"]
    assert record.attrs["name"] == form_data[1]["value"]
    assert record.attrs["reply"] == form_data[2]["value"]
