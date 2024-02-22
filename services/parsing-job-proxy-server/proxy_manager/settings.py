from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ##################
    # storage 관련된 코드
    ##################
    storage_endpoint_url: str = Field(description="object storage의 endpoint url")
    storage_access_key: str = Field(description="object storage의 access key")
    storage_secret_key: str = Field(description="object storage의 secret key")
    storage_raw_data_bucket_name: str = Field(description="원 데이터가 저장되어 있는 bucket name")
    storage_prep_data_bucket_name: str = Field(description="전처리된 데이터가 저장되어 있는 bucket name")

    # .env 파일을 읽어들이는 세팅
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


def load_settings():
    """ settings 정보 가져오기
    환경 변수와 .env 파일을 통해 정보를 불러오는 함수

    :return:
    """
    return Settings()
