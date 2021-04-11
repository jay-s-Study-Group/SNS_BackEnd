from dataclasses import dataclass
from os import path, environ
from typing import List

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


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
    DB_URL: str = environ.get(
        "DEFAULT_DB_URL", "mysql+pymysql://travis@localhost/notification_api?charset=utf8mb4"
    )


@dataclass
class LocalConfig(Config):
    DATABASE_HOST = environ.get("LOCAL_DB_HOST", "localhost")
    DATABASE_PASSWD = environ.get("LOCAL_DB_PASSWORD", "")
    DATABASE_USER = environ.get("LOCAL_DB_USER", "root")
    DATABASE_PORT = environ.get("LOCAL_DB_PORT", 3306)
    PROJ_RELOAD = True
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class ProdConfig(Config):
    DATABASE_HOST = environ.get("PROD_DB_HOST", "localhost")
    DATABASE_PASSWD = environ.get("PROD_DB_PASSWORD", "")
    DATABASE_USER = environ.get("PROD_DB_USER", "root")
    DATABASE_PORT = environ.get("PROD_DB_PORT", 3306)
    PROJ_RELOAD = False
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


@dataclass
class TestConfig(Config):
    DB_URL: str = environ.get(
        "TEST_DB_URL", "mysql+pymysql://travis@localhost/notification_api?charset=utf8mb4"
    )
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True


def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("API_ENV", "local")]()