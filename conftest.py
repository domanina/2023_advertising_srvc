import pytest

from services.my_srvc.my_srvc_api import SrvcApi


@pytest.fixture(scope="session")
def srvc_api_client():
    api = SrvcApi()
    yield api
