import uvicorn
from fastapi import FastAPI
from app.common.util import conf
from app.api import api_router


def create_app():
    """
    FastAPI 앱 변수 생성 후 반환
    :return:
    fastApi App
    """
    config = conf()

    app = FastAPI()
    app.include_router(api_router)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=conf().WEB_SERVER_PORT,
        reload=conf().PROJ_RELOAD,
    )
