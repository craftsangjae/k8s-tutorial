import logging
from datetime import datetime, timedelta

import fire
import yfinance

from proxy_manager.configuration import load_proxy_configurations, StorageSettings
from proxy_manager.storage import FinanceDataStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 스토리지에 대한 configuration만 호출
config = load_proxy_configurations(StorageSettings)

# 데이터 스토리지 로드하기
# (1) RAW 데이터 저장소
raw_storage = FinanceDataStorage(
    endpoint_url=config.storage_endpoint_url,
    access_key=config.storage_access_key,
    secret_key=config.storage_secret_key,
    bucket_name=config.storage_raw_data_bucket_name
)


def main(
        ticker: str,
        start_date_str: str,
        end_date_str: str
):
    """ preloading_job의 메인함수로 아래 순으로 실행
    (1) yfinance에서 티커에 대한 원 데이터
    (2) 필요한 필드만 추출
    (3) 데이터 업로드

    :param ticker: 티겟아이디
    :param start_date_str: 시작일자. (2022/01/01, 2022-01-01, 20220101) 와 같은 패턴을 가져야 함
    :param end_date_str: 종료일자. (2022/01/01, 2022-01-01, 20220101) 와 같은 패턴을 가져야 함
    :return:
    """

    c_date = parse_date(str(start_date_str))
    end_date = parse_date(str(end_date_str))

    while c_date <= end_date:
        yahoo_df = yfinance.download(
            ticker,
            start=c_date,
            end=c_date + timedelta(days=1),
            interval="1m"
        )
        raw_df = yahoo_df[['Open', 'High', 'Low', 'Close']]

        raw_storage.upload(ticker, c_date, raw_df)
        c_date += timedelta(days=1)


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
