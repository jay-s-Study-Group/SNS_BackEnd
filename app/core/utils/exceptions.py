class StatusCode:
    HTTP_100_CONTINUE = 100
    HTTP_101_SWITCHING_PROTOCOLS = 101
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_202_ACCEPTED = 202
    HTTP_203_NON_AUTHORITATIVE_INFORMATION = 203
    HTTP_204_NO_CONTENT = 204
    HTTP_205_RESET_CONTENT = 205
    HTTP_206_PARTIAL_CONTENT = 206
    HTTP_207_MULTI_STATUS = 207
    HTTP_300_MULTIPLE_CHOICES = 300
    HTTP_301_MOVED_PERMANENTLY = 301
    HTTP_302_FOUND = 302
    HTTP_303_SEE_OTHER = 303
    HTTP_304_NOT_MODIFIED = 304
    HTTP_305_USE_PROXY = 305
    HTTP_306_RESERVED = 306
    HTTP_307_TEMPORARY_REDIRECT = 307
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_402_PAYMENT_REQUIRED = 402
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_405_METHOD_NOT_ALLOWED = 405
    HTTP_406_NOT_ACCEPTABLE = 406
    HTTP_407_PROXY_AUTHENTICATION_REQUIRED = 407
    HTTP_408_REQUEST_TIMEOUT = 408
    HTTP_409_CONFLICT = 409
    HTTP_410_GONE = 410
    HTTP_411_LENGTH_REQUIRED = 411
    HTTP_412_PRECONDITION_FAILED = 412
    HTTP_413_REQUEST_ENTITY_TOO_LARGE = 413
    HTTP_414_REQUEST_URI_TOO_LONG = 414
    HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
    HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE = 416
    HTTP_417_EXPECTATION_FAILED = 417
    HTTP_422_UNPROCESSABLE_ENTITY = 422
    HTTP_423_LOCKED = 423
    HTTP_424_FAILED_DEPENDENCY = 424
    HTTP_425_TOO_EARLY = 425
    HTTP_428_PRECONDITION_REQUIRED = 428
    HTTP_429_TOO_MANY_REQUESTS = 429
    HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS = 451
    HTTP_500_INTERNAL_SERVER_ERROR = 500
    HTTP_501_NOT_IMPLEMENTED = 501
    HTTP_502_BAD_GATEWAY = 502
    HTTP_503_SERVICE_UNAVAILABLE = 503
    HTTP_504_GATEWAY_TIMEOUT = 504
    HTTP_505_HTTP_VERSION_NOT_SUPPORTED = 505
    HTTP_507_INSUFFICIENT_STORAGE = 507
    HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = 511



class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_503_SERVICE_UNAVAILABLE,
        code: str = "000000",
        obj: str = None,
        msg: str = None,
        detail: str = None,
        ex: Exception = None,
        ):
        self.status_code = status_code
        self.code = code
        self.obj = obj
        self.msg = msg
        self.detail = detail
        super().__init__(ex)

class NotFoundUserEx(APIException):
    def __init__(self, user_id: str = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="유저 정보를 찾을 수 없습니다.",
            detail=f"Not Found User | Token : {user_id}",
            code=f"{StatusCode.HTTP_500_INTERNAL_SERVER_ERROR}{'1'.zfill(4)}",
            ex=ex,
        )

class NotFoundMentoringEx(APIException):
    def __init__(self, user_id: int = None, mentoring_id: int = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="멘토링 정보를 찾을 수 없습니다.",
            detail=f"Not Found Mentoring | user_id : {user_id}, input_mentor_id : {mentoring_id}",
            code=f"{StatusCode.HTTP_500_INTERNAL_SERVER_ERROR}{'1'.zfill(4)}",
            ex=ex,
        )

class NotFoundClassTypeEx(APIException):
    def __init__(self, user_id: int = None, class_type_name: str = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="존재 하지 않는 클래스 형식입니다.",
            detail=f"Not Exist class Form. | user_id : {user_id}, input_class_type_name : {class_type_name}",
            code=f"{StatusCode.HTTP_500_INTERNAL_SERVER_ERROR}{'1'.zfill(4)}",
            ex=ex,
        )

class AleadyRegisterEx(APIException):
    def __init__(self, email: int = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_503_SERVICE_UNAVAILABLE,
            msg="이미 가입된 이메일입니다.",
            detail=f"이미 가입된 이메일입니다. | UserEmail : {email}",
            code=f"{StatusCode.HTTP_503_SERVICE_UNAVAILABLE}{'1'.zfill(4)}",
            ex=ex,
        )

class ExternalEx(APIException):
    def __init__(self, status_code: int = None, text: str = None, ex: Exception = None):
        super().__init__(
            status_code=status_code,
            msg=text,
            detail=text,
            code=f"{status_code}{'1'.zfill(4)}",
            ex=ex,
        )

class DeleteUserEx(APIException):
    def __init__(self, email: int = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_503_SERVICE_UNAVAILABLE,
            msg="삭제된 회원입니다.",
            detail=f"삭제된 회원입니다. | UserEmail : {email}",
            code=f"{StatusCode.HTTP_503_SERVICE_UNAVAILABLE}{'1'.zfill(4)}",
            ex=ex,
        )

class NotAllowedTokenEx(APIException):
    def __init__(self, email: int = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_503_SERVICE_UNAVAILABLE,
            msg="허용되지 않은 토큰 값입니다.",
            detail=f"허용되지 않은 토큰 값입니다. | UserEmail : {email}",
            code=f"{StatusCode.HTTP_503_SERVICE_UNAVAILABLE}{'1'.zfill(4)}",
            ex=ex,
        )