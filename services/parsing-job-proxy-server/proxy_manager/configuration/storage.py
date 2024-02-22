from pydantic import Field

from proxy_manager.configuration.common import CommonSettings


class StorageSettings(CommonSettings):
    ##################
    # storage 관련된 설정
    ##################
    storage_endpoint_url: str = Field(description="object storage의 endpoint url")
    storage_access_key: str = Field(description="object storage의 access key")
    storage_secret_key: str = Field(description="object storage의 secret key")
    storage_raw_data_bucket_name: str = Field(description="원 데이터가 저장되어 있는 bucket name")
    storage_prep_data_bucket_name: str = Field(description="전처리된 데이터가 저장되어 있는 bucket name")
