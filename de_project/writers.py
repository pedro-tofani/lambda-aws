import datetime
import json
import os
from tempfile import NamedTemporaryFile
import boto3

from dotenv import dotenv_values

config = dotenv_values(".env")
ACCESS_KEY = config.get("ACCESS_KEY")
SECRET_KEY = config.get("SECRET_KEY")
BUCKET_S3 = config.get("BUCKET_S3")


class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion"
        super().__init__(self.message)


class DataWriter:
    def __init__(self, currency: str, date: datetime.date) -> None:
        self.currency = currency
        self.date = date

    @property
    def filename(self):
        file_end = f"{self.date.year}-{self.date.month}-{self.date.day}"
        return f"./data/{self.currency}/{self.date.year}/{file_end}.json"

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "a") as f:
            f.write(row)

    def write(self, data: dict) -> None:
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        else:
            raise DataTypeNotSupportedForIngestionException(data)


class S3Writer(DataWriter):
    def __init__(self, currency: str, date: datetime.date) -> None:
        super().__init__(currency, date)
        self.tempfile = NamedTemporaryFile()
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
        )

    @property
    def filename(self):
        file_end = f"{self.date.year}-{self.date.month}-{self.date.day}"
        return f"coin={self.currency}/year={self.date.year}/date={file_end}.json"

    def _write_row(self, row: str) -> None:
        with open(self.tempfile.name, "a") as f:
            f.write(str(row))

    def write(self, data):
        self._write_row(row=data)
        self.s3.put_object(Body=self.tempfile, Bucket=BUCKET_S3, Key=self.filename)
