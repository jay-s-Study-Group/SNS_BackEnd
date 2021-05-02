import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.middlewares.authentication import JWTAuthenticationBackend
from app.core.middlewares.token_validator import access_control
from app.core.config import load_config
from app.api import api_router

CONFIG = load_config()


def create_app():
    """
    FastAPI 앱 변수 생성 후 반환
    :return:
    fastApi App
    """
    app = FastAPI()
    app.include_router(api_router)
    app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend())
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    return app


app = create_app()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=CONFIG.WEB_SERVER_PORT,
        reload=CONFIG.PROJ_RELOAD,
    )
