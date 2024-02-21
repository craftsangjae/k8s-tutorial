import pandas as pd
import pytest as pytest

from src.exception import NotFoundDataException, InvalidDataFormatException
from src.storage import FinanceDataStorage
from pytest_mock import MockerFixture
from datetime import date


@pytest.fixture
def data_storage():
    return FinanceDataStorage("http://localhost:9000", "123", "123", "hello")


def test_raise_exception_when_try_to_download_file_that_doesnt_exist(
        data_storage: FinanceDataStorage,
        mocker: MockerFixture
):
    mocker.patch("src.storage.FinanceDataStorage.exist", return_value=False)

    with pytest.raises(NotFoundDataException):
        data_storage.download("ticker", date(2022, 3, 11))


def test_download_file_if_file_exists(
        data_storage: FinanceDataStorage,
        mocker: MockerFixture
):
    mocker.patch("src.storage.FinanceDataStorage.exist", return_value=True)
    mocker.patch("src.storage.BaseObjectStorage.download_object", return_value=b"Open,High,Low,Close\n1,1,1,1\n2,2,2,2")

    df = data_storage.download("ticker", date(2022, 3, 11))
    assert df.loc[0, 'Open'] == 1
    assert df.loc[1, 'Open'] == 2


def test_raise_exception_when_Open_field_is_missing(
        data_storage: FinanceDataStorage,
):
    df = pd.DataFrame({
        # "Open": [1, 2, 3],
        "Close": [1, 2, 3],
        "High": [1, 2, 3],
        "Low": [1, 2, 3]
    })
    with pytest.raises(InvalidDataFormatException):
        data_storage.upload("ticker", date(2022, 3, 11), df)


def test_raise_exception_when_field_dt_is_not_numeric(
        data_storage: FinanceDataStorage
):
    df = pd.DataFrame({
        "Open": ["1", "2", "3"],
        "Close": [1, 2, 3],
        "High": [1, 2, 3],
        "Low": [1, 2, 3]
    })
    with pytest.raises(InvalidDataFormatException):
        data_storage.upload("ticker", date(2022, 3, 11), df)


def test_upload_success(
        data_storage: FinanceDataStorage,
        mocker: MockerFixture
):
    df = pd.DataFrame({
        "Open": [1, 2, 3],
        "Close": [1, 2, 3],
        "High": [1, 2, 3],
        "Low": [1, 2, 3]
    })
    mocker.patch("src.storage.FinanceDataStorage.upload_object", return_value=None)

    data_storage.upload("ticker", date(2022, 3, 11), df)
