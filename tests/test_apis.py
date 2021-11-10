import datetime

from src.apis import HistoryCurrencyApi, HistoryCryptoApi, ResponseApi

import pytest
from unittest.mock import patch
import requests

from dotenv import dotenv_values

config = dotenv_values(".env")
TOKEN = config.get("TOKEN")


class TestHistoryCurrencyApi:
    @pytest.mark.parametrize(
        "date, coin, expected",
        [
            (
                datetime.date(2020, 1, 4),
                "EUR",
                f"http://api.exchangeratesapi.io/v1/2020-01-04?access_key={TOKEN}&base=EUR",
            ),
            (
                datetime.date(2020, 11, 21),
                "BLR",
                f"http://api.exchangeratesapi.io/v1/2020-11-21?access_key={TOKEN}&base=BLR",
            ),
        ],
    )
    def test_get_endpoint_HistoryCurrencyApi(self, date, coin, expected):
        api = HistoryCurrencyApi(coin=coin)
        endpoint = api._get_endpoint({"date": date})

        assert endpoint == expected

    def test_adjust_response_HistoryCurrencyApi(self):
        api = HistoryCurrencyApi(coin="test")
        response = {
            "rates": {"BTC": 1, "ETH": 2},
            "date": "2020-01-04",
            "timestamp": "123456789",
        }

        adjusted_response = api._adjust_response(data=response)
        expected_response = {
            "BTC": 1,
            "date": "2020-01-04",
            "ETH": 2,
            "timestamp": "123456789",
        }

        assert adjusted_response == expected_response


class TestHistoryCryptoApi:
    @pytest.mark.parametrize(
        "date, coin, expected",
        [
            (
                datetime.date(2020, 1, 4),
                "BTC",
                "https://www.mercadobitcoin.net/api/BTC/day-summary/2020/1/4",
            ),
            (
                datetime.date(2020, 11, 21),
                "BTC",
                "https://www.mercadobitcoin.net/api/BTC/day-summary/2020/11/21",
            ),
            (
                datetime.date(2020, 1, 4),
                "ETH",
                "https://www.mercadobitcoin.net/api/ETH/day-summary/2020/1/4",
            ),
        ],
    )
    def test_get_endpoint_HistoryCryptoApi(self, date, coin, expected):
        api = HistoryCryptoApi(coin=coin)
        endpoint = api._get_endpoint({"date": date})

        assert endpoint == expected

    def test_adjust_response_HistoryCryptoApi(self):
        api = HistoryCryptoApi(coin="test")
        response = {
            "rates": 2,
            "date": "2020-01-04",
            "timestamp": "123456789",
        }

        adjusted_response = api._adjust_response(data=response)

        assert adjusted_response == response

    def test_if_raises_error(self):
        api = HistoryCryptoApi(coin="test")
        with pytest.raises(Exception):
            api._adjust_response(data=None)


@pytest.fixture()
@patch("src.apis.ResponseApi.__abstractmethods__", set())
def fixture_test_api():
    return ResponseApi(coin="test")


def mocked_requests_get(*args, **kwargs):
    class MockResponse(requests.Response):
        def __init__(self, json_data, status_code):
            super().__init__()
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            return self.json_data

        def raise_for_status(self) -> None:
            if self.status_code != 200:
                raise Exception

    if args[0] == "valid_endpoint":
        return MockResponse(json_data={"foo": "bar"}, status_code=200)
    else:
        return MockResponse(json_data=None, status_code=404)


class TestAPI:
    @patch("requests.get")
    @patch(
        "src.apis.ResponseApi._get_endpoint",
        return_value="valid_endpoint",
    )
    def test_get_data_requests_is_called(
        self, mock_get_endpoint, mock_requests, fixture_test_api
    ):
        fixture_test_api.get_data()
        mock_requests.assert_called_once_with("valid_endpoint")

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch(
        "src.apis.ResponseApi._get_endpoint",
        return_value="valid_endpoint",
    )
    @patch(
        "src.apis.ResponseApi._adjust_response",
        return_value={"foo": "bar"},
    )
    def test_get_data_with_valid_endpoint(
        self, mock_adjust_response, mock_get_endpoint, mock_requests, fixture_test_api
    ):
        actual = fixture_test_api.get_data()
        expected = {"foo": "bar"}
        assert actual == expected

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch(
        "src.apis.ResponseApi._get_endpoint",
        return_value="invalid_endpoint",
    )
    @patch(
        "src.apis.ResponseApi._adjust_response",
        return_value={"foo": "bar"},
    )
    def test_get_data_with_invalid_endpoint(
        self, mock_adjust_response, mock_get_endpoint, mock_requests, fixture_test_api
    ):
        with pytest.raises(Exception):
            fixture_test_api.get_data()
