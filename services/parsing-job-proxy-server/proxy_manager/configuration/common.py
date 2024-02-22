from typing import TypeVar, cast

from pydantic_settings import BaseSettings, SettingsConfigDict

from proxy_manager.exceptions import MissingConfigException

# 공통 설정 클래스에 대한 TypeVar 생성
T = TypeVar('T', bound='CommonSettings')


class CommonSettings(BaseSettings):
    # extra='ignore' 하지 않으면, 다른 환경변수가 들어올때 에러 발생
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    def __add__(self: T, other: T) -> T:
        if not isinstance(other, CommonSettings):
            raise MissingConfigException(f"{other}은 CommonSettings 인스턴스가 아닙니다.")

        # 현재 인스턴스와 다른 인스턴스의 필드 값을 병합
        combined_fields = {**self.dict(), **other.dict()}

        # 병합된 필드로 새로운 인스턴스 생성
        # `cast`를 사용하여 반환 타입을 명시적으로 지정
        return cast(T, self.__class__(**combined_fields))
