from abc import ABC, abstractmethod


class DataIngestor(ABC):
    def __init__(self, writer, currency, api, dates_list) -> None:
        self.writer = writer
        self.currency = currency
        self.api = api
        self.dates_list = dates_list

    @abstractmethod
    def ingest(self) -> None:
        pass


class CurrencyIngestorByDate(DataIngestor):
    def ingest(self) -> None:
        for date in self.dates_list:
            api = self.api(coin=self.currency)
            data = api.get_data(date=date)
            self.writer(date=date, currency=self.currency).write(data)
