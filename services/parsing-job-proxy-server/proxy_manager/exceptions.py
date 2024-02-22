class CommonException(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class NotFoundDataException(CommonException):
    """ 데이터가 존재하지 않을 때 에러
    """
    pass


class NotReadyBucketException(CommonException):
    """ 버킷이 존재하지 않을 때 에러
    """
    pass


class InvalidDataFormatException(CommonException):
    """ 잘못된 데이터 포맷을 가졌을 때 에러
    """
    pass


class MissingConfigException(CommonException):
    """ 환경설정 정보가 잘못되었을 때 에러
    """
    pass


class FailedJobRequestException(CommonException):
    """ job에 대한 호출이 실패되었을 때 에러
    """
    pass


class NotExistJobException(CommonException):
    """ 존재하지 않은 job에 접근할 때 에러
    """
    pass


class AlreadyExistedJobException(CommonException):
    """ 이미 존재하고 있는 job에 대해 생성 시도할 때 에러
    """
    pass
