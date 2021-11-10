from datetime import datetime
from ingestor import CurrencyIngestorByDate
from writers import DataWriter
from apis import HistoryCryptoApi


def get_dates_list(year):
    date_list = [
        datetime.strptime(f"{year}-{month}-1", "%Y-%m-%d") for month in range(1, 13)
    ]
    return date_list


if __name__ == "__main__":
    year_summary_ingestor = CurrencyIngestorByDate(
        writer=DataWriter,
        currency="BTC",
        api=HistoryCryptoApi,
        dates_list=get_dates_list(2020),
    )
    year_summary_ingestor.ingest()
