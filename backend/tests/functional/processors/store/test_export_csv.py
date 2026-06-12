from datetime import datetime
from io import StringIO

import csv
import pytest


@pytest.fixture
def document_blocks() -> dict:
    return {
        "form-id": {
            "@type": "schemaForm",
            "store": True,
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


@pytest.fixture
def answers() -> list[dict]:
    return [
        {
            "data": {
                "message": "just want to say hi",
                "name": "John",
                "foo": "skip this",
            },
            "block_id": "form-id",
        },
        {
            "data": {"message": "bye", "name": "Sally"},
            "block_id": "form-id",
        },
    ]


class TestDataStore:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.url = "/document"

    def test_export_csv(self, submit_form, export_csv, answers):
        for answer in answers:
            response = submit_form(
                path=self.url,
                data=answer,
                commit=True,
            )
            assert response.status_code == 200

        response = export_csv(self.url)
        data = [*csv.reader(StringIO(response.text), delimiter=",")]
        assert len(data) == 3
        assert data[0] == ["Message", "Name", "date"]
        sorted_data = sorted(data[1:])
        assert sorted_data[0][:-1] == ["bye", "Sally"]
        assert sorted_data[1][:-1] == ["just want to say hi", "John"]

        # check date column. Skip seconds because can change during test
        now = datetime.now().strftime("%Y-%m-%dT%H:%M")
        assert sorted_data[0][-1].startswith(now)
        assert sorted_data[1][-1].startswith(now)
