import logging

from datetime import datetime
from de_project.ingestor import CurrencyIngestorByDate
from de_project.writers import S3Writer
from de_project.apis import HistoryCryptoApi


def get_dates_list(year):
    date_list = [
        datetime.strptime(f"{year}-{month}-1", "%Y-%m-%d") for month in range(1, 13)
    ]
    return date_list


def lambda_handler(event, context):
    logging.info(f"event received: {event}")
    logging.info(f"context received: {context}")

    year_summary_ingestor = CurrencyIngestorByDate(
        writer=S3Writer,
        currency="BTC",
        api=HistoryCryptoApi,
        dates_list=get_dates_list(2020),
    )
    year_summary_ingestor.ingest()
