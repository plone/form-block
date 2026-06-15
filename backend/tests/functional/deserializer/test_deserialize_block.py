from copy import deepcopy

import pytest
import transaction


class TestBlockDeserialization:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal):
        self.portal = portal
        self.document = portal.document
        self.url = "/document"

    def test_deserializer_cleanup_data_in_send_message_field(self, manager_request):
        new_blocks = deepcopy(self.document.blocks)
        new_blocks["form-id"]["send_message"] = (
            "<b onmouseover=\"alert('XSS testing!')\">click here</b><p><i>keep tags</i></p>"
        )
        manager_request.patch(
            self.url,
            json={"blocks": new_blocks},
        )
        transaction.commit()
        blocks = self.document.blocks
        assert (
            blocks["form-id"]["send_message"]
            == "<b>click here</b><p><i>keep tags</i></p>"
        )
