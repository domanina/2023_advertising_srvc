import random
import string
import allure

from dataclasses import asdict
from deepdiff import DeepDiff
from consts.consts import TypeString
from services.my_srvc.models.ItemChangeReq import ItemChange
from services.my_srvc.models.ItemSegment import ItemSegment
from datetime import datetime, timezone


def generate_random_string(length: int, string_type: str) -> str:
    if string_type == TypeString.CHAR_NUM_UPPER.value:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    elif string_type == TypeString.CHAR_NUM_LOWER.value:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    elif string_type == TypeString.CHAR_UPPER.value:
        return ''.join(random.choices(string.ascii_uppercase, k=length))
    elif string_type == TypeString.CHAR_LOWER.value:
        return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_expected_body(item_change_request: ItemChange, response: dict) -> ItemSegment:
    expected_body = ItemSegment()
    expected_body.id = response["id"]
    expected_body.json = response["json"]
    expected_body.channel_name = item_change_request.itemChange.channel
    expected_body.segment_type = item_change_request.itemChange.segmentType
    expected_body.segment_length = item_change_request.itemChange.segmentLength
    expected_body.current_time = item_change_request.itemChange.currentTime
    expected_body.createdAt = f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"
    expected_body.updatedAt = expected_body.createdAt
    return expected_body


def assert_dates(expected: str, actual: str):
    date_time_obj1 = datetime.strptime(expected, "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()
    date_time_obj2 = datetime.strptime(actual, "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()
    assert (date_time_obj1-date_time_obj2) < 5, \
        f"Test failed. Difference between dates is more than 5 seconds.\nExpected: {expected}, actual: {actual}"


@allure.step
def assert_body(expected: dict, actual: dict, excluded: list):
    ddiff = DeepDiff(expected, actual, ignore_order=True, exclude_paths=excluded)
    assert not ddiff, f"Test failed. different actual body : {ddiff}"


def assert_segments(expected_list: list[ItemSegment], response: dict):
    actual_list = [ItemSegment(**item) for item in response]
    for actual_segment in actual_list:
        for expected_segment in expected_list:
            if actual_segment.id == expected_segment.id:
                assert_dates(expected_segment.createdAt, actual_segment.createdAt)
                assert_body(asdict(expected_segment), asdict(actual_segment), ["createdAt", "updatedAt"])

