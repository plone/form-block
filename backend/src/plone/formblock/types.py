from typing import Any
from typing import TypedDict


class FieldInfo(TypedDict):
    field_id: str
    label: str


class FieldData(TypedDict):
    field_id: str
    value: Any
