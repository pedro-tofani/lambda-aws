from abc import ABC, abstractmethod

from dotenv import dotenv_values

import logging
import ratelimit
import requests
from backoff import on_exception, expo

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

config = dotenv_values(".env")
TOKEN = config.get("TOKEN")


class ResponseApi(ABC):
    """
    [Abstract class for the differents APIs]
    """

    def __init__(self, coin: str) -> None:
        self.coin = coin

    @abstractmethod
    def _get_endpoint(self, coin, **kwargs) -> str:
        """[Abstrac method to return the endpoint]

        Args:
            coin ([string]): [The desired coin/currency]

        Returns:
            str: [The respective endpoint]
        """
        pass

    @abstractmethod
    def _adjust_response(self, **kwargs) -> dict:
        """[Abstrac method to adjust the API's response]

        Returns:
            dict: [The adjusted response in a dictionary]
        """
        pass

    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=60, period=60)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def get_data(self, **kwargs) -> dict:
        """[Method to call the API. It has some tools to handle exceptions and to avoid several API's
            calls in a short time]

        Returns:
            dict: [data adjusted from the API]
        """
        endpoint = self._get_endpoint(kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")

        response = requests.get(endpoint)
        response.raise_for_status()
        response_json = response.json()

        data = self._adjust_response(data=response_json)
        return data


class HistoryCurrencyApi(ResponseApi):
    def _get_endpoint(self, date: dict) -> str:
        year = date["date"].year
        month = date["date"].month
        day = date["date"].day
        date_formatted = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
        base_url = "http://api.exchangeratesapi.io/v1/"
        return f"{base_url}{date_formatted}?access_key={TOKEN}&base={self.coin}"

    def _adjust_response(self, data: dict) -> str:
        adjusted_data = data["rates"]
        adjusted_data["date"] = data["date"]
        adjusted_data["timestamp"] = data["timestamp"]
        return adjusted_data


class HistoryCryptoApi(ResponseApi):
    def _get_endpoint(self, date: dict) -> str:
        year = date["date"].year
        month = date["date"].month
        day = date["date"].day
        return f"https://www.mercadobitcoin.net/api/{self.coin}/day-summary/{year}/{month}/{day}"

    def _adjust_response(self, data: dict) -> str:
        if not data:
            raise Exception("No data found")
        return data
