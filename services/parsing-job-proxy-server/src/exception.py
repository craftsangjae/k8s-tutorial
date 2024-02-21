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
