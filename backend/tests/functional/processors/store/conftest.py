import pytest


@pytest.fixture
def export_data(manager_request):
    def func(url):
        url = f"{url}/@form-data"
        response = manager_request.get(url)
        return response

    return func


@pytest.fixture
def export_csv(manager_request):
    def func(url):
        url = f"{url}/@form-data-export"
        response = manager_request.get(url)
        return response

    return func


@pytest.fixture
def clear_data(manager_request):
    def func(url):
        url = f"{url}/@form-data-clear"
        response = manager_request.delete(url)
        return response

    return func
