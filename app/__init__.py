from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.middlewares.authentication import JWTAuthenticationBackend
from app.core.middlewares.token_validator import access_control
from app.api import api_router


def init_router(app: FastAPI):
    app.include_router(api_router)


def init_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_middleware(app: FastAPI):
    app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend())
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)


def init_listener(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )


def create_app():
    """
    FastAPI 앱 변수 생성 후 반환
    :return:
    fastApi App
    """
    app = FastAPI()
    init_router(app)
    init_cors(app)
    init_middleware(app)
    init_listener(app)
    return app


app = create_app()
