from datetime import datetime
from plone.dexterity.content import DexterityContent
from plone.formblock import types as t
from plone.formblock.interfaces import IFormDataStore
from souper.soup import Record
from zope.component import getMultiAdapter


def get_schema_fields_from_block(block: dict) -> list[t.FieldInfo]:
    """Get the form fields for the current block."""
    block_type = block.get("@type", "")
    if block_type == "schemaForm":
        return [
            {"field_id": name, "label": field.get("title", name)}
            for name, field in block["schema"]["properties"].items()
        ]
    return []


def record_from_form_data(
    data: list[t.FieldData], block_id: str, form_fields: list[t.FieldInfo]
) -> Record:
    fields = {
        x["field_id"]: x.get("custom_field_id", x.get("label", x["field_id"]))
        for x in form_fields
    }
    record = Record()
    fields_labels = {}
    fields_order = []
    for field_data in data:
        field_id = field_data.get("field_id", "")
        value = field_data.get("value", "")
        if field_id in fields:
            record.attrs[field_id] = value
            fields_labels[field_id] = fields[field_id]
            fields_order.append(field_id)
    record.attrs["fields_labels"] = fields_labels
    record.attrs["fields_order"] = fields_order
    record.attrs["date"] = datetime.now()
    record.attrs["block_id"] = block_id
    return record


def total_records_in_block(context: DexterityContent, block_id: str) -> int:
    """Return all records in a data manager given block_id."""
    data_manager = getMultiAdapter((context, block_id), IFormDataStore)

    return data_manager.length()
