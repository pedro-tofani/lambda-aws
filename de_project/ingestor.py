from abc import ABC, abstractmethod


class DataIngestor(ABC):
    """
    [Abstract class for the differents Igestors]
    """

    def __init__(self, writer, currency, api, dates_list) -> None:
        """[Init function]

        Args:
            writer ([src.writers.DataWriter]): [Required writer]
            currency ([str]): [The desired coin/currency]
            api ([src.apis.ResponseApi]): [Required API]
            dates_list ([dict]): [Dict continig the dates to be processed]
        """
        self.writer = writer
        self.currency = currency
        self.api = api
        self.dates_list = dates_list

    @abstractmethod
    def ingest(self) -> None:
        """
        [Abstrac method to ingest the data]
        """
        pass


class CurrencyIngestorByDate(DataIngestor):
    def ingest(self) -> None:
        for date in self.dates_list:
            api = self.api(coin=self.currency)
            data = api.get_data(date=date)
            self.writer(date=date, currency=self.currency).write(data)
