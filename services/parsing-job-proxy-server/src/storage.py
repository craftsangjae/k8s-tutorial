from io import StringIO

import boto3
import pandas as pd
from datetime import date
from src.exception import NotReadyBucketException, CommonException, InvalidDataFormatException, NotFoundDataException
from botocore.exceptions import ClientError
from pandas.api.types import is_numeric_dtype


class BaseObjectStorage:
    def __init__(
            self,
            endpoint_url: str,
            access_key: str,
            secret_key: str,
            bucket_name: str
    ):
        """ object storage에 업로드 / 다운로드 하는 클래스

        :param endpoint_url:
        :param access_key:
        :param secret_key:
        :param bucket_name:
        """
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3',
                                 endpoint_url=endpoint_url,
                                 aws_access_key_id=access_key,
                                 aws_secret_access_key=secret_key)
        self.bucket = self.s3.Bucket(self.bucket_name)

    def exists_key(self, key) -> bool:
        try:
            self.bucket(key).load()
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise CommonException("storage에 Object.load()을 수행하는 중 실패가 발행했습니다.")

    def download_object(self, key: str) -> bytes:
        try:
            obj = self.bucket.Object(key)
            return obj.get()['Body'].read()
        except ClientError:
            raise CommonException("object.get()을 수행하는 중 오류가 발생했습니다")

    def upload_object(self, key: str, body: str) -> None:
        try:
            self.bucket.Object(key).put(Body=body)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucket':
                raise NotReadyBucketException(f"버킷({self.bucket_name})이 생성되지 않았습니다.")
            raise CommonException("storage에 Object.put()을 수행하는 중 실패가 발생했습니다.")


class FinanceDataStorage(BaseObjectStorage):
    """ Finance Data을 관리하는 Object Storage 클래스

    :method
    - download: 데이터 다운로드
    - upload: 데이터 업로드
    - exist: 데이터 존재하는지 체크

    bucket 내에 아래와 같은 구조로 데이터가 저장되어 있음
    <ticker name>/<date>.csv
    ex:
    KRWUSD/20240201.csv
    KRWUSD/20240202.csv
    KRWUSD/20240203.csv
    ...

    """

    def download(self, ticker: str, data_date: date) -> pd.DataFrame:
        """ ticker & data_date에 해당하는 데이터 다운로드
        없는 경우, NotFoundError 보내기

        :param ticker:
        :param data_date:
        :return: pd.DataFrame
        finance data
        """
        if not self.exist(ticker, data_date):
            raise NotFoundDataException(f"{self.to_key(ticker, data_date)} 키가 존재하지 않습니다.")

        csv_string = self.download_object(self.to_key(ticker, data_date)).decode('utf-8')
        return pd.read_csv(StringIO(csv_string))

    def upload(self, ticker: str, data_date: date, data_df: pd.DataFrame) -> None:
        """ 데이터 업로드, 잘못된 포맷의 경우 에러 반환

        :param ticker:
        :param data_date:
        :param data_df:
        :return:
        """
        self._validate(data_df)

        key = self.to_key(ticker, data_date)
        body = self.to_csv_string(data_df)

        self.upload_object(key, body)

    def exist(self, ticker: str, data_date: date) -> bool:
        """ 주어진 데이터가 스토리지에 존재하는지 조회
        :param ticker:
        :param data_date:
        :return:
        """
        key = self.to_key(ticker, data_date)
        return self.exists_key(key)

    @classmethod
    def _validate(cls, data_df: pd.DataFrame):
        """ 데이터의 포맷이 정상적인지 검증
        - required columns : [Open, High, Low, Close]
        - required datatype: float

        :param data_df: 주가 정보로 되어 있는지를 검증
        :return:
        """
        necessary_fields = {"Open", "High", "Low", "Close"}
        if necessary_fields - set(data_df.columns):
            raise InvalidDataFormatException("필수 컬럼이 존재하지 않습니다.")

        for field in necessary_fields:
            if not is_numeric_dtype(data_df[field]):
                raise InvalidDataFormatException("데이터 필드가 숫자형이 아닙니다.")

    @classmethod
    def to_key(cls, ticker: str, data_date: date) -> str:
        """ ticker와 data_date로 key 경로 구성

        :param ticker:
        :param data_date:
        :return:
        """
        return f"{ticker}/{data_date.strftime('%Y%m%d')}.csv"

    @classmethod
    def to_csv_string(cls, data_df: pd.DataFrame):
        """ 데이터를 csv 포맷으로 변경 """
        return data_df.to_csv(index=False)
