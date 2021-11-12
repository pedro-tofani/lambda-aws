import pytest
from de_project.crypto_call import get_dates_list
from datetime import datetime


class TestCrypto_Call:
    @pytest.mark.parametrize(
        "year, expected",
        [
            (
                2020,
                [
                    datetime.strptime("2020-1-1", "%Y-%m-%d"),
                    datetime.strptime("2020-2-1", "%Y-%m-%d"),
                    datetime.strptime("2020-3-1", "%Y-%m-%d"),
                    datetime.strptime("2020-4-1", "%Y-%m-%d"),
                    datetime.strptime("2020-5-1", "%Y-%m-%d"),
                    datetime.strptime("2020-6-1", "%Y-%m-%d"),
                    datetime.strptime("2020-7-1", "%Y-%m-%d"),
                    datetime.strptime("2020-8-1", "%Y-%m-%d"),
                    datetime.strptime("2020-9-1", "%Y-%m-%d"),
                    datetime.strptime("2020-10-1", "%Y-%m-%d"),
                    datetime.strptime("2020-11-1", "%Y-%m-%d"),
                    datetime.strptime("2020-12-1", "%Y-%m-%d"),
                ],
            ),
            (
                2019,
                [
                    datetime.strptime("2019-1-1", "%Y-%m-%d"),
                    datetime.strptime("2019-2-1", "%Y-%m-%d"),
                    datetime.strptime("2019-3-1", "%Y-%m-%d"),
                    datetime.strptime("2019-4-1", "%Y-%m-%d"),
                    datetime.strptime("2019-5-1", "%Y-%m-%d"),
                    datetime.strptime("2019-6-1", "%Y-%m-%d"),
                    datetime.strptime("2019-7-1", "%Y-%m-%d"),
                    datetime.strptime("2019-8-1", "%Y-%m-%d"),
                    datetime.strptime("2019-9-1", "%Y-%m-%d"),
                    datetime.strptime("2019-10-1", "%Y-%m-%d"),
                    datetime.strptime("2019-11-1", "%Y-%m-%d"),
                    datetime.strptime("2019-12-1", "%Y-%m-%d"),
                ],
            ),
        ],
    )
    def test_get_dates_list(self, year, expected):
        result = get_dates_list(year)
        assert result == expected
