import allure

from requests import Response
from services.api_client.api_client import ApiClient
from config.config import URL, TECH_USER, TECH_TOKEN
from tools.singleton import Singleton


class SrvcApi(ApiClient, metaclass=Singleton):
    def __init__(self, url=URL, user=TECH_USER, token=TECH_TOKEN):
        super().__init__(url=url, user=user, token=token)

    @allure.step("Get health check")
    def get_health(self, auth) -> Response:
        path = "/"
        return self._get(path=path, auth=auth, json=None)

    @allure.step("Get  one item")
    def get_data(self, item, auth, params: dict) -> Response:
        path = f".../{item}"
        return self._get(path=path, auth=auth, json=None, params=params)

    @allure.step("Get all items")
    def get_all_data(self, auth) -> Response:
        path = "/..."
        return self._get(path=path, auth=auth, json=None)

    @allure.step
    def post_data(self, payload: dict, auth) -> Response:
        path = "/my_srvc"
        return self._post(path=path, json=payload, auth=auth)
