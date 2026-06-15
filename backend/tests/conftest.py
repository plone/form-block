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
