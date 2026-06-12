import pytest


@pytest.fixture
def document_blocks() -> dict:
    return {
        "form-id": {
            "@type": "schemaForm",
            "store": True,
        }
    }


class TestDataStore:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.url = "/document"

    def test_unable_to_store_data(self, submit_form):
        """Empty form data, unable to store data"""

        response = submit_form(
            path=self.url,
            data={
                "block_id": "form-id",
            },
            commit=True,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Empty form data."
