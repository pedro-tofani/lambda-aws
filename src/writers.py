import datetime
import json
import os


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
