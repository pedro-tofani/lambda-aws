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
    """
    [Custom exception made to throw an error of not expected data type]
    """

    def __init__(self, data):
        """[Init function, iherits from Exception class]

        Args:
            data ([str]): [Type of data that is not supported]
        """
        self.message = f"Data type {data} is not supported for ingestion"
        super().__init__(self.message)


class DataWriter:
    """[Data Writer class. Responsible for receiving the data and saving it somewhere]"""

    def __init__(self, currency: str, date: datetime.date) -> None:
        """[Init function]

        Args:
            currency (str): [The desired coin/currency]
            date (datetime.date): [datetime to save the filename]
        """
        self.currency = currency
        self.date = date

    @property
    def filename(self) -> str:
        """[Property. Returns the filename to be used]

        Returns:
            [str]: [filename string]
        """
        file_end = f"{self.date.year}-{self.date.month}-{self.date.day}"
        return f"./data/{self.currency}/{self.date.year}/{file_end}.json"

    def _write_row(self, row: str) -> None:
        """[internal function to write the row]

        Args:
            row (str): [desired row to be written]
        """
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "a") as f:
            f.write(row)

    def write(self, data: dict) -> None:
        """[Function that is called to start the writing process. Verify the data type]

        Args:
            data (dict): [Data to be written]

        Raises:
            DataTypeNotSupportedForIngestionException: [Exception if data type is not supported]
        """
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        else:
            raise DataTypeNotSupportedForIngestionException(type(data))


class S3Writer(DataWriter):
    """[Writer that is used to write the extracted that into S3 instance]

    Args:
        DataWriter ([src.writers.DataWriter]): [The writer that this class inherits properties from]
    """

    def __init__(self, currency: str, date: datetime.date) -> None:
        """[Inherits from DataWriter and add two properties: a tempfile and an S3 instance connection
            using boto3]

        Args:
            currency (str): [description]
            date (datetime.date): [description]
        """
        super().__init__(currency, date)
        self.tempfile = NamedTemporaryFile()
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
        )

    @property
    def filename(self) -> str:
        """[Overrides the filename property to return the filename to be used in S3]

        Returns:
            [str]: [filename string]
        """
        file_end = f"{self.date.year}-{self.date.month}-{self.date.day}"
        return f"coin={self.currency}/year={self.date.year}/date={file_end}.json"

    def _write_row(self, row: str) -> None:
        """[Internal function to write the row]

        Args:
            row (str): [row to be written in the tempfile]
        """
        with open(self.tempfile.name, "a") as f:
            f.write(str(row))

    def write(self, data):
        """[Overrides the write function to write the data to the tempfile and then to S3]

        Args:
            data ([str]): [dat obe writen]
        """
        self._write_row(row=data)
        self.s3.put_object(Body=self.tempfile, Bucket=BUCKET_S3, Key=self.filename)
