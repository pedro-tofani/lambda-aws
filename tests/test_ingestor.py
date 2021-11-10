from unittest.mock import patch, call
from src.ingestor import CurrencyIngestorByDate
from src.apis import HistoryCryptoApi
from src.writers import DataWriter


class TestHistoryCurrencyApi:
    @patch("src.apis.HistoryCryptoApi.get_data", return_value="data_getted")
    @patch("src.writers.DataWriter.write", return_value="written_data")
    def test_CurrencyIngestorByDate(self, mock_write, mock_get_data):
        ingestor = CurrencyIngestorByDate(
            writer=DataWriter,
            currency="TEST",
            api=HistoryCryptoApi,
            dates_list=["date1", "date2"],
        )
        ingestor.ingest()
        mock_write.assert_called_with("data_getted")
        mock_get_data.assert_has_calls([call(date="date1"), call(date="date2")])
