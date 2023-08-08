import json
import allure

from requests import Response
from jsonschema import validate
from consts.consts import Colors
from tools.logger import get_logger

logger = get_logger(name="main_logger")


@allure.step
def valid_schema(data: object, schema_file: str):
    with open(schema_file) as f:
        schema = json.load(f)
        validate(instance=data, schema=schema)


@allure.step
def check_status_code(response: Response, status_code: int):
    assert response.status_code == status_code, \
        f"Test failed. HTTP status is : {response.status_code}, {response.text} (expected  HTTP status: {status_code})"


def pretty_log_request(response: Response, method: str, **kwargs):
    logger.info(f"{Colors.GREEN.value}{method} request to {response.url}{Colors.BLACK.value}")
    if kwargs.get("json") is not None:
        logger.info(f"{Colors.GREEN.value}Request body is {kwargs.get('json')}{Colors.BLACK.value}")
    logger.info(f"Response status is: {response.status_code}")
    logger.info(f"Response body is {response.text}")
