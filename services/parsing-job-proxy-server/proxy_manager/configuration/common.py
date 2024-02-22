from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    # extra='ignore' 하지 않으면, 다른 환경변수가 들어올때 에러 발생
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


class CombinedSettings:
    """ 복수개의 BaseSettings을 병합하여 setting 정보를 제공하는 클래스
    """
    __dict__ = {}

    def __init__(self, *settings):
        for s in settings:
            self.__dict__.update(s)
        for k, v in self.__dict__.items():
            setattr(self, k, v)

    def __iter__(self):
        """
        so `dict(model)` works
        """
        yield from self.__dict__.items()
