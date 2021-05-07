import base64
import hmac
import time
import traceback
import typing
import re
import jwt
import datetime
from jwt.exceptions import ExpiredSignatureError, DecodeError
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.core.utils.exceptions import APIException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.core.middlewares.api_logger import api_logger

EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/auth)"
EXCEPT_PATH_LIST = ["/", "/openapi.json"]


def to_dict(data):
    return data.__dict__["__data__"]


async def access_control(request: Request, call_next):
    request.state.req_time = datetime.date.today()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    request.state.service = None

    ip = (
        request.headers["x-forwarded-for"]
        if "x-forwarded-for" in request.headers.keys()
        else request.client.host
    )
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    headers = request.headers
    cookies = request.cookies

    url = request.url.path
    if await url_pattern_check(url, EXCEPT_PATH_REGEX) or url in EXCEPT_PATH_LIST:
        response = await call_next(request)
        if url != "/":
            await api_logger(request=request, response=response)
        return response

    try:
        if url.startswith("/test"):
            # test 인경우 헤더로 토큰 검사 => 너가 원하는대로 고쳐서 쓰면 됨
            if url.startswith("/api/services"):
                qs = str(request.query_params)
                qs_list = qs.split("&")

                response = await call_next(request)
                return response

        else:
            # 템플릿 렌더링인 경우 쿠키에서 토큰 검사
            cookies["Authorization"] = "Bearer"

        response = await call_next(request)
        await api_logger(request=request, response=response)
    except APIException as e:
        response = await test_exception_handler(e)
        await api_logger(request=request, error=e)
    except Exception as e:

        error = await exception_handler(e)

        # error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
        # response = JSONResponse(status_code=error.status_code, content=error_dict)
        print(e.args)
        print(traceback.format_exc())
        error.status_code, content = HTTP_500_INTERNAL_SERVER_ERROR, {
            "statusCode": 500,
            "error": "Bad Request",
            "message": "잠시 후 다시 시도해 주시길 바랍니다.",
        }
        response = JSONResponse(status_code=error.status_code, content=content)
        try:
            request.errorMessage = e.args
        except:
            pass
        await api_logger(request=request, error=error)

    return response


async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def exception_handler(error: Exception):
    print(error)
    return error


async def test_exception_handler(error: APIException):
    error_dict = dict(
        status=error.status_code, msg=error.msg, detail=error.detail, code=error.code
    )
    res = JSONResponse(status_code=error.status_code, content=error_dict)
    return res
