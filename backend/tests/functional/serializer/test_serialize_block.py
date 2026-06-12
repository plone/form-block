import pytest


class TestBlockSerialization:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        document = portal.document
        self.blocks = document.blocks
        self.url = "/document"

    def test_serializer_return_full_block_data_to_admin(self, manager_request):
        response = manager_request.get(self.url)
        res = response.json()
        assert res["blocks"]["form-id"] == self.blocks["form-id"]

    def test_serializer_return_filtered_block_data_to_anon(self, anon_request):
        response = anon_request.get(self.url)
        res = response.json()
        assert res["blocks"]["form-id"] != self.blocks["form-id"]
        assert "sender_name" in res["blocks"]["form-id"]
        assert "sender" in res["blocks"]["form-id"]
        assert "default_name" not in res["blocks"]["form-id"]
        assert "default_from" not in res["blocks"]["form-id"]
        assert "schema" in res["blocks"]["form-id"]
