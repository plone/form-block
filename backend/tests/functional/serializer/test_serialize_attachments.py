import pytest


class TestBlockSerialization:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.url = "/document"

    def test_serializer_without_attachments_limit(self, anon_request):
        response = anon_request.get(self.url)
        res = response.json()
        assert "attachments_limit" not in res["blocks"]["form-id"]
