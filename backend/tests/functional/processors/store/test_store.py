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


class TestDataStore:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.url = "/document"

    def test_store_data(self, submit_form, export_data, export_csv, clear_data):
        response = submit_form(
            path=self.url,
            data={
                "data": {
                    "message": "just want to say hi",
                    "name": "John",
                    "foo": "skip this",
                },
                "block_id": "form-id",
            },
            commit=True,
        )
        assert response.status_code == 200
        response = export_data(self.url)
        data = response.json()
        assert len(data["items"]) == 1
        item = data["items"][0]
        assert sorted(item.keys()) == [
            "__expired",
            "block_id",
            "date",
            "id",
            "message",
            "name",
        ]
        assert item["message"] == {"label": "Message", "value": "just want to say hi"}
        assert item["name"] == {"label": "Name", "value": "John"}
        response = submit_form(
            path=self.url,
            data={
                "data": {"message": "bye", "name": "Sally"},
                "block_id": "form-id",
            },
            commit=True,
        )
        assert response.status_code == 200
        response = export_data(self.url)
        data = response.json()
        assert len(data["items"]) == 2
        for item in data["items"]:
            assert sorted(item.keys()) == [
                "__expired",
                "block_id",
                "date",
                "id",
                "message",
                "name",
            ]
        sorted_data = sorted(data["items"], key=lambda x: x["name"]["value"])
        assert sorted_data[0]["name"]["value"] == "John"
        assert sorted_data[0]["message"]["value"] == "just want to say hi"
        assert sorted_data[1]["name"]["value"] == "Sally"
        assert sorted_data[1]["message"]["value"] == "bye"

        # clear data
        response = clear_data(self.url)
        assert response.status_code == 204
        response = export_csv(self.url)
        data = [*csv.reader(StringIO(response.text), delimiter=",")]
        assert len(data) == 1
        assert data[0] == ["date"]
