import uvicorn
from fastapi import FastAPI
from app.utils.config import load_config
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
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=CONFIG.WEB_SERVER_PORT,
        reload=CONFIG.PROJ_RELOAD,
    )
