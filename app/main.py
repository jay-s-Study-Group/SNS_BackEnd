import uvicorn
from fastapi import FastAPI

from app.common.util import conf
from dotenv import load_dotenv
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
    load_dotenv(verbose=True)
    uvicorn.run("main:app", host="0.0.0.0", port=3052, reload=conf().PROJ_RELOAD)
