import time
import pytest

from config.config import AUTH, WRONG_CREDS
from consts.consts import Colors, TIMEOUT_SEC
from services.my_srvc.models.ItemChangeReq import ItemChangeSegment, SegmentType
from helpers.helper import *
from dataclasses import asdict
from http import HTTPStatus
from tools.helper import check_status_code
from tools.logger import get_logger

logger = get_logger(name="main_logger")


@allure.suite("POST tests")
class TestPost:
    @pytest.mark.parametrize("segment_type",
                             [
                                 type.value for type in SegmentType]
                             + [generate_random_string(10, TypeString.CHAR_LOWER.value), "can be space"])
    @allure.title("POST valid segmentType data")
    def test_post_data_segment_type(self, srvc_api_client, segment_type):
        program_change = ItemChange(
            itemChange=ItemChangeSegment(segmentType=segment_type, channel=generate_random_string(10, TypeString.CHAR_NUM_UPPER.value)))
        response = srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
        with allure.step("Compare expected and actual results"):
            check_status_code(response, HTTPStatus.OK)
            expected = generate_expected_body(program_change, response.json())
            actual = ItemSegment(**response.json())
            assert_dates(expected.createdAt, actual.createdAt)
            assert_body(asdict(expected), asdict(actual), ["createdAt", "updatedAt"])

    @pytest.mark.parametrize("segment_type",
                             [type.value.upper() for type in SegmentType] +
                             [
                                 generate_random_string(10, TypeString.CHAR_NUM_UPPER.value),
                                 generate_random_string(10, TypeString.CHAR_NUM_LOWER.value),
                                 "",
                                 " ",
                                 " first space",
                                 "last space ",
                                 "in_valid",
                                 "-+=!§>?{}|",
                                 None,
                                 0,
                                 -1,
                                 876589,
                                 True,
                                 False
                              ])
    @allure.title("POST invalid segmentType data")
    def test_post_data_invalid_segment_type(self, srvc_api_client, segment_type):
        program_change = ItemChange(
            itemChange=ItemChangeSegment(segmentType=segment_type, channel=generate_random_string(10, TypeString.CHAR_NUM_UPPER.value)))
        response = srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
        with allure.step("Compare expected and actual results"):
            check_status_code(response, HTTPStatus.BAD_REQUEST)

    @pytest.mark.parametrize("channel_name",
                             [
                                 generate_random_string(10, TypeString.CHAR_NUM_UPPER.value),
                                 generate_random_string(10, TypeString.CHAR_UPPER.value),
                                 "0001_TEST_CH"])
    @allure.title("POST valid item name data")
    def test_post_data_item_name(self, srvc_api_client, name):
        program_change = ItemChange(
            itemChange=ItemChangeSegment(segmentType=SegmentType.UNKNOWN.value,
                                         channel=name))
        response = srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
        with allure.step("Compare expected and actual results"):
            check_status_code(response, HTTPStatus.OK)
            expected = generate_expected_body(program_change, response.json())
            actual = ItemSegment(**response.json())
            assert_dates(expected.createdAt, actual.createdAt)
            assert_body(asdict(expected), asdict(actual), ["createdAt", "updatedAt"])

    @pytest.mark.parametrize("name",
                             [
                                 generate_random_string(10, TypeString.CHAR_NUM_LOWER.value),
                                 generate_random_string(10, TypeString.CHAR_NUM_LOWER.value),
                                 "",
                                 " ",
                                 "with space",
                                 " first_space",
                                 "last_space ",
                                 "in-valid",
                                 "-+=!§>?{}|",
                                 "86567896754",
                                 None,
                                 0,
                                 -1,
                                 876589,
                                 True,
                                 False
                             ])
    @allure.title("POST invalid channel name data")
    def test_post_data_invalid_channel(self, srvc_api_client, name):
        program_change = ItemChange(
            itemChange=ItemChangeSegment(segmentType=SegmentType.UNKNOWN.value,
                                         channel=name))
        response = srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
        with allure.step("Compare expected and actual results"):
            check_status_code(response, HTTPStatus.BAD_REQUEST)

    @pytest.mark.parametrize("current_time", [1, 168989898998898])
    @allure.title("POST valid currentTime data")
    def test_post_data_current_time(self, srvc_api_client, current_time):
        program_change = ItemChange(
            itemChange=ItemChangeSegment(segmentType=SegmentType.UNKNOWN.value,
                                         channel=generate_random_string(10, TypeString.CHAR_NUM_UPPER.value),
                                         currentTime=current_time)
        )
        response = srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
        with allure.step("Compare expected and actual results"):
            check_status_code(response, HTTPStatus.OK)
            expected = generate_expected_body(program_change, response.json())
            actual = ItemSegment(**response.json())
            assert_dates(expected.createdAt, actual.createdAt)
            assert_body(asdict(expected), asdict(actual), ["createdAt", "updatedAt"])

    @pytest.mark.parametrize("current_time",
                             [
                                 generate_random_string(10, TypeString.CHAR_NUM_LOWER.value),
                                 "",
                                 " ",
                                 "-+=!§>?{}|",
                                 "86567896754",
                                 None,
                                 0,
                                 -1,
                                 7676.676,
                                 1689898989988989956465,
                                 True,
                                 False
                             ])
    @allure.title("POST invalid currentTime data")
    def test_post_data_invalid_current_time(self, srvc_api_client, current_time):
        program_change = ItemChange(
            itemChange=ItemChangeSegment(segmentType=SegmentType.UNKNOWN.value,
                                         channel=generate_random_string(10, TypeString.CHAR_NUM_UPPER.value),
                                         currentTime=current_time)
        )
        response = srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
        with allure.step("Compare expected and actual results"):
            check_status_code(response, HTTPStatus.BAD_REQUEST)

    @pytest.mark.parametrize("segment_length", [1, 1689898989988989])
    @allure.title("POST valid segmentLength data")
    def test_post_data_segment_length(self, srvc_api_client, segment_length):
        program_change = ItemChange(
            itemChange=ItemChangeSegment(segmentType=SegmentType.UNKNOWN.value,
                                         channel=generate_random_string(10, TypeString.CHAR_NUM_UPPER.value),
                                         segmentLength=segment_length)
        )
        response = srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
        with allure.step("Compare expected and actual results"):
            check_status_code(response, HTTPStatus.OK)
            expected = generate_expected_body(program_change, response.json())
            actual = ItemSegment(**response.json())
            assert_dates(expected.createdAt, actual.createdAt)
            assert_body(asdict(expected), asdict(actual), ["createdAt", "updatedAt"])

    @pytest.mark.parametrize("segment_length",
                             [
                                 generate_random_string(10, TypeString.CHAR_NUM_LOWER.value),
                                 "",
                                 " ",
                                 "-+=!§>?{}|",
                                 "86567896754",
                                 None,
                                 0,
                                 -1,
                                 1689898989988989956465,
                                 7676.676,
                                 True,
                                 False
                             ])
    @allure.title("POST invalid segmentLength data")
    def test_post_data_invalid_segment_length(self, srvc_api_client, segment_length):
        program_change = ItemChange(
            itemChange=ItemChangeSegment(segmentType=SegmentType.UNKNOWN.value,
                                         channel=generate_random_string(10, TypeString.CHAR_NUM_UPPER.value),
                                         segmentLength=segment_length)
        )
        response = srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
        with allure.step("Compare expected and actual results"):
            check_status_code(response, HTTPStatus.BAD_REQUEST)

    @pytest.mark.parametrize("body",
                             [
                                 {'programChange': {}},
                               ...
                             ])
    @allure.title("POST invalid body (without every field)")
    def test_post_body_invalid(self, srvc_api_client, body):
        response = srvc_api_client.post_data(payload=body, auth=AUTH)
        with allure.step("Compare expected and actual results"):
            check_status_code(response, HTTPStatus.BAD_REQUEST)


@allure.suite("GET tests")
class TestGet:

    @allure.title("Ping Eventstream srvc")
    def test_get_health(self, srvc_api_client):
        response = srvc_api_client.get_health(auth=AUTH)
        check_status_code(response, HTTPStatus.OK)

    @pytest.mark.parametrize("wrong_creds", WRONG_CREDS)
    @allure.title("Get access denied error")
    def test_access_denied(self, srvc_api_client, wrong_creds):
        response = srvc_api_client.get_health(auth=wrong_creds)
        check_status_code(response, HTTPStatus.FORBIDDEN)

    @allure.title("Get all channels data")
    def test_get_all_data(self, srvc_api_client):
        response = srvc_api_client.get_all_data(auth=AUTH)
        check_status_code(response, HTTPStatus.OK)

    @pytest.mark.parametrize("wrong_creds", WRONG_CREDS)
    @allure.title("Get all data - access denied")
    def test_get_all_data_access_denied(self, srvc_api_client, wrong_creds):
        response = srvc_api_client.get_all_data(auth=wrong_creds)
        check_status_code(response, HTTPStatus.FORBIDDEN)

    @pytest.mark.parametrize("channel_name",
                             [
                                 generate_random_string(10, TypeString.CHAR_NUM_UPPER.value),
                                 generate_random_string(10, TypeString.CHAR_UPPER.value),
                                 "0001_TEST_CH"])
    @allure.title("Get channel data")
    def test_get_channel_data(self, srvc_api_client, channel_name):
        expected_list = []
        with allure.step("POST new channel"):
            program_change = ItemChange(
                itemChange=ItemChangeSegment(segmentType=SegmentType.PROGRAM.value, channel=channel_name)
            )
            new_channel = srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
            expected = generate_expected_body(program_change, new_channel.json())
            expected_list.append(expected)
        with allure.step("GET info about posted channel"):
            response = srvc_api_client.get_data(channel=channel_name, auth=AUTH, params=None)
            check_status_code(response, HTTPStatus.OK)
        with allure.step("Compare expected and actual results"):
            assert_segments(expected_list, response.json())

    @pytest.mark.parametrize("wrong_creds", WRONG_CREDS)
    @allure.title("Get channel data - access denied")
    def test_get_channel_data_access_denied(self, srvc_api_client, wrong_creds):
        response = srvc_api_client.get_data(channel="PRO7MAXX", params=None, auth=wrong_creds)
        check_status_code(response, HTTPStatus.FORBIDDEN)

    @pytest.mark.parametrize("channel_name",
                             [
                                 generate_random_string(10, TypeString.CHAR_NUM_LOWER.value),
                                 generate_random_string(10, TypeString.CHAR_LOWER.value),
                                 "0001-TEST-CH",
                                 "889909808",
                                 "0001 TEST CH",
                                 "pro7maxx",
                                 878798,
                                 False,
                                 True
                             ])
    @allure.title("Get channel data - invalid channel name")
    def test_get_invalid_channel_data(self, srvc_api_client, channel_name):
        response = srvc_api_client.get_data(channel=channel_name, auth=AUTH, params=None)
        check_status_code(response, HTTPStatus.BAD_REQUEST)

    @pytest.mark.parametrize("channel", ["NOT_EXIST", "888_TEST"])
    @allure.title("Get channel data - not exist channel - empty list")
    def test_get_empty_channel_data(self, srvc_api_client, channel):
        response = srvc_api_client.get_data(channel=channel, auth=AUTH, params=None)
        check_status_code(response, HTTPStatus.OK)
        assert response.text == "[]", logger.error(f"{Colors.RED.value}Test failed. Wrong response body: {response.text}{Colors.BLACK.value}")

    @allure.title("Get channel data with few segments")
    def test_get_few_channel_data(self, srvc_api_client):
        channel_name = generate_random_string(10, TypeString.CHAR_NUM_UPPER.value)
        expected_list = []
        with allure.step("POST new channel info"):
            for segment_type in SegmentType:
                program_change = ItemChange(
                    itemChange=ItemChangeSegment(segmentType=segment_type.value, channel=channel_name)
                )
                new_channel = srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
                expected = generate_expected_body(program_change, new_channel.json())
                expected_list.append(expected)
        with allure.step("GET info about posted channel"):
            response = srvc_api_client.get_data(channel=channel_name, auth=AUTH, params=None)
            check_status_code(response, HTTPStatus.OK)
        with allure.step("Compare expected and actual results"):
            assert_segments(expected_list, response.json())

    @allure.title("Get channel data with utcstart/utcend - get every from 5")
    def test_get_channel_data_with_query(self, srvc_api_client):
        channel_name = generate_random_string(10, TypeString.CHAR_NUM_UPPER.value)
        all_expected_list = []
        with allure.step("POST new channel info"):
            for segment_type in SegmentType:
                program_change = ItemChange(
                    itemChange=ItemChangeSegment(segmentType=segment_type.value, channel=channel_name)
                )
                new_channel = srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
                expected = generate_expected_body(program_change, new_channel.json())
                all_expected_list.append(expected)
                time.sleep(TIMEOUT_SEC)
        with allure.step("GET info about posted channel"):
            current_expected_list = []
            for segment in all_expected_list:
                current_expected_list.append(segment)
                params = {"utcstart": "2023-05-23T10:47:28", "utcend": segment.createdAt[:-5]}
                response = srvc_api_client.get_data(channel=channel_name, auth=AUTH, params=params)
                check_status_code(response, HTTPStatus.OK)
                with allure.step("Compare expected and actual results"):
                    assert_segments(current_expected_list, response.json())

    @pytest.mark.parametrize("utcstart, utcend",
                             [
                                 ("2023-05-23T10:47:28", "2023-05-23T10:50:28"),
                                 ("2027-05-23T10:47:28", "2027-05-23T10:50:28"),
                                 ("2023-05-23T10:50:28", "2023-05-23T10:47:28"),
                                 ("2023-05-23T10:50:28", None)

                             ])
    @allure.title("Get channel data with utcstart/utcend - empty list")
    def test_get_empty_channel_data_with_query(self, srvc_api_client, utcstart, utcend):
        channel_name = generate_random_string(10, TypeString.CHAR_NUM_UPPER.value)
        with allure.step("POST new channel info"):
            program_change = ItemChange(
                    itemChange=ItemChangeSegment(segmentType=SegmentType.UNKNOWN.value, channel=channel_name))
            srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
        with allure.step("GET info about posted channel"):
            params = {"utcstart": utcstart, "utcend": utcend}
            response = srvc_api_client.get_data(channel=channel_name, auth=AUTH, params=params)
            check_status_code(response, HTTPStatus.OK)
            assert response.text == "[]", logger.error(f"{Colors.RED.value}Test failed. Wrong response body: {response.text}{Colors.BLACK.value}")

    @pytest.mark.parametrize("utcstart, utcend",
                             [
                                 ("2023-06-01T08:17:02.043Z", "2023-06-01T08:17:03.043Z"),
                                 ("2027-5-23T10:47:28", "2027-5-23T10:50:28"),
                                 ("2023-05-23T10:50", "2023-05-23T10:47"),
                                 (None, "2023-05-23T10:50:28"),
                                 (1685600415, 1685600420),
                                 ("test", None)
                             ])
    @allure.title("Get channel data with invalid utcstart/utcend")
    def test_get_channel_data_with_invalid_query(self, srvc_api_client, utcstart, utcend):
        channel_name = generate_random_string(10, TypeString.CHAR_NUM_UPPER.value)
        with allure.step("POST new channel info"):
            program_change = ItemChange(
                itemChange=ItemChangeSegment(segmentType=SegmentType.UNKNOWN.value, channel=channel_name))
            srvc_api_client.post_data(payload=asdict(program_change), auth=AUTH)
        with allure.step("GET info about posted channel"):
            params = {"utcstart": utcstart, "utcend": utcend}
            response = srvc_api_client.get_data(channel=channel_name, auth=AUTH, params=params)
            check_status_code(response, HTTPStatus.BAD_REQUEST)
