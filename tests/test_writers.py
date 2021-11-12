from datetime import datetime

from de_project.writers import DataWriter, DataTypeNotSupportedForIngestionException
from unittest.mock import patch, mock_open

import pytest
import json


@pytest.fixture
def writer_fixture():
    date = datetime.strptime("09/05/2020", "%d/%m/%Y")
    return DataWriter(currency="EUR", date=date)


class TestDataWriter:
    @patch("builtins.open", new_callable=mock_open, read_data="")
    @patch("de_project.writers.DataWriter.filename", return_value="file_name")
    def test_write_row(self, mock_file_name, mock_open_file, writer_fixture):
        writer_fixture._write_row({"a": 1, "b": 2})
        mock_open_file.assert_called_with(mock_file_name, "a")

    def test_write_not_dict_fail(self, writer_fixture):
        with pytest.raises(DataTypeNotSupportedForIngestionException):
            writer_fixture.write(["test"])

    @patch("de_project.writers.DataWriter._write_row", return_value="foobar")
    def test_write(self, mock_write_row, writer_fixture):
        response_json = {"a": 1, "b": 2}
        writer_fixture.write(response_json)
        mock_write_row.assert_called_with(json.dumps(response_json) + "\n")

    def test_filename(self, writer_fixture):
        assert writer_fixture.filename == "./data/EUR/2020/2020-5-9.json"
