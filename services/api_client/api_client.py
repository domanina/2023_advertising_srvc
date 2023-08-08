import requests

from requests import request, Response
from requests.auth import HTTPBasicAuth
from consts.consts import Colors
from tools.helper import pretty_log_request
from tools.logger import get_logger

logger = get_logger(name="main_logger")


class ApiClient:
    def __init__(self, url: str, user: str, token: str):
        assert url and user and token, "Url, User and Password must be set"
        self._url = url
        self._user = user
        self._token = token
        self._auth = HTTPBasicAuth(username=self._user, password=self._token)

    @property
    def url(self):
        return self._url

    def _perform_request(self, method: str, path: str, auth: HTTPBasicAuth, **kwargs) -> Response:
        headers = {
            "Accept": "application/json"
        }
        url = self.url + path

        try:
            response = request(method=method, url=url, headers=headers, auth=auth, verify=False, **kwargs)
            pretty_log_request(response=response, method=method, **kwargs)
            return response
        except requests.RequestException as e:
            logger.exception(f"\n{Colors.RED.value}Request to '{path}' failed: {e}{Colors.BLACK.value}")

    def _get(self, path: str, auth: HTTPBasicAuth | None = None, **kwargs):
        auth = auth or self._auth
        return self._perform_request("GET", path, auth, **kwargs)

    def _post(self, path: str, auth: HTTPBasicAuth | None = None, **kwargs):
        auth = auth or self._auth
        return self._perform_request("POST", path, auth, **kwargs)

    def _delete(self, path: str, **kwargs):
        return self._perform_request("DELETE", path, **kwargs)

    def _put(self, path: str, **kwargs):
        return self._perform_request("PUT", path, **kwargs)