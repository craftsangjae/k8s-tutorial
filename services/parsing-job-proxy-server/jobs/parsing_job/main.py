import logging
from datetime import datetime, timedelta
from typing import List

import fire
import pandas as pd

from proxy_manager.configuration import StorageSettings
from proxy_manager.exceptions import NotFoundDataException
from proxy_manager.storage import FinanceDataStorage, BaseObjectStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 스토리지에 대한 환경 설정 가져오기
settings = StorageSettings()

# 데이터 스토리지 로드하기
raw_storage = FinanceDataStorage(
    endpoint_url=settings.storage_endpoint_url,
    access_key=settings.storage_access_key,
    secret_key=settings.storage_secret_key,
    bucket_name=settings.storage_raw_data_bucket_name
)

preprocess_storage = BaseObjectStorage(
    endpoint_url=settings.storage_endpoint_url,
    access_key=settings.storage_access_key,
    secret_key=settings.storage_secret_key,
    bucket_name=settings.storage_prep_data_bucket_name
)


def main(
        ticker: str,
        start_date_str: str,
        end_date_str: str,
        save_path: str
):
    """ parsing_job의 메인함수로 아래 순으로 실행
    (1) 다운로드 수행
    (2) 전처리 수행
    (3) 파싱 데이터 업로드

    :param ticker: 티겟아이디
    :param start_date_str: 시작일자. (2022/01/01, 2022-01-01, 20220101) 와 같은 패턴을 가져야 함
    :param end_date_str: 종료일자. (2022/01/01, 2022-01-01, 20220101) 와 같은 패턴을 가져야 함
    :param save_path: 완료된 데이터가 저장될 공간
    :return:
    """
    downloaded_dfs = download_objects_in_range(ticker, start_date_str, end_date_str)
    parsed_data = parse_raw_data(downloaded_dfs)
    upload_parsed_data(parsed_data, save_path)


def download_objects_in_range(ticker: str, start_date_str: str, end_date_str: str):
    """ 두 날짜 범위에 존재하는 모든 데이터 가져오기

    :param ticker:
    :param start_date_str: 시작일
    :param end_date_str: 종료일
    :return:
    """
    global raw_storage
    logger.info(f"ticker:{ticker}에서 {start_date_str}~{end_date_str}까지의 데이터를 가져옵니다.")

    c_date = parse_date(str(start_date_str))
    end_date = parse_date(str(end_date_str))

    downloaded = []
    while c_date <= end_date:
        logger.info(f"{c_date} 다운로드 중...")
        df = raw_storage.download(ticker, c_date)
        downloaded.append(df)
        c_date += timedelta(days=1)

    if len(downloaded) == 0:
        # 병합할 데이터 존재하지 않음
        raise NotFoundDataException("데이터가 존재하지 않습니다.")

    return downloaded


def parse_raw_data(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """ 데이터를 원하는 형태로 정규화

    :param dfs:
    :return:
    """
    df = pd.concat(dfs)
    df.index = pd.to_datetime(df.index)
    df = df[~df.index.duplicated(keep='first')]
    full_df = df.resample('1T')
    return full_df.interpolate(method='linear')


def upload_parsed_data(df: pd.DataFrame, save_path: str):
    """ 파싱된 데이터를 업로드

    :param df:
    :param save_path:
    :return:
    """
    global preprocess_storage
    logging.info(f"데이터를 {save_path}로 업로드합니다.")
    data = df.to_parquet()
    preprocess_storage.upload_object(save_path, data)


def parse_date(date_str: str):
    formats = ['%Y-%m-%d', '%Y%m%d', '%Y/%m/%d']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass
    raise ValueError("Invalid date format")


if __name__ == '__main__':
    fire.Fire(main)
