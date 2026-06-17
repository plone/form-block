from pathlib import Path
from plone.formblock.testing import FUNCTIONAL_TESTING
from plone.formblock.testing import INTEGRATION_TESTING
from pytest_plone import fixtures_factory

import pytest


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory((
        (FUNCTIONAL_TESTING, "functional"),
        (INTEGRATION_TESTING, "integration"),
    ))
)


@pytest.fixture(scope="session")
def resources_path() -> Path:
    tests_folder = Path(__file__).parent
    return tests_folder / "_resources"


@pytest.fixture(scope="session")
def resource_file(resources_path: Path):
    def func(filename: str) -> Path:
        return resources_path / filename

    return func


@pytest.fixture
def form_data_store_factory(portal, http_request):
    from plone.formblock.datamanager.catalog import FormDataStore

    def factory(context=None, block_id=""):
        if context is None:
            context = portal
        request = http_request
        data_store = FormDataStore(context, request)
        data_store._block_id = block_id
        return data_store

    return factory
