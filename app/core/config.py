from dataclasses import dataclass
from os import path, environ
from typing import List
from dotenv import load_dotenv

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
load_dotenv(verbose=True)


@dataclass
class Config:
    """
    기본 Configuration
    """

    BASE_DIR: str = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DEBUG: bool = False
    TEST_MODE: bool = False
    JWT_SECRET_KEY: str = environ.get("JWT_SECRET_KEY", "thisissecretkey!@#$")
    JWT_ALGORITHM: str = environ.get("JWT_ALGORITHM", "HS256")
    SLACK_TOKEN = 'xoxb-1929181904582-2022675902579-qNO3xuYLSUscjfXcr5yjTvs4'
    KAKAO_API_CLIENT_ID: str = environ.get("KAKAO_API_CLIENT_ID")
    KAKAO_OAUTH_REDIRECT_URI: str = environ.get(
        "KAKAO_OAUTH_REDIRECT_URI", "http://127.0.0.1:3052/sns/kakao/oauth-token"
    )
    WEB_SERVER_PORT: int = int(environ.get("WEB_SERVER_PORT", 3052))


@dataclass
class LocalConfig(Config):
    DB_URL: str = environ.get(
        "LOCAL_DB_URL", "mysql+pymysql://root@localhost/dbname?charset=utf8mb4"
    )
    DATABASE_NAME = environ.get("LOCAL_DB_NAME", "test")
    DATABASE_HOST = environ.get("LOCAL_DB_HOST", "localhost")
    DATABASE_PASSWD = environ.get("LOCAL_DB_PASSWORD", "")
    DATABASE_USER = environ.get("LOCAL_DB_USER", "root")
    DATABASE_PORT = int(environ.get("LOCAL_DB_PORT", 3306))
    SLACK_TOKEN = 'xoxb-1929181904582-2022675902579-qNO3xuYLSUscjfXcr5yjTvs4'
    PROJ_RELOAD = True
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class ProdConfig(Config):
    DB_URL: str = environ.get(
        "PROD_DB_URL", "mysql+pymysql://root@localhost/dbname?charset=utf8mb4"
    )
    DATABASE_NAME = environ.get("PROD_DB_NAME", "test")
    DATABASE_HOST = environ.get("PROD_DB_HOST", "localhost")
    DATABASE_PASSWD = environ.get("PROD_DB_PASSWORD", "")
    DATABASE_USER = environ.get("PROD_DB_USER", "root")
    DATABASE_PORT = int(environ.get("PROD_DB_PORT", 3306))
    SLACK_TOKEN = ''
    PROJ_RELOAD = False
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


@dataclass
class TestConfig(Config):
    DB_URL: str = environ.get(
        "TEST_DB_URL",
        "mysql+pymysql://travis@localhost/notification_api?charset=utf8mb4",
    )
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True


def load_config():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("API_ENV", "local")]()
