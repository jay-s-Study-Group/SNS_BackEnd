import hashlib
import secrets
import bcrypt
from functools import lru_cache


@lru_cache
def get_hasher(algorithm="default"):
    if algorithm == "default":
        return BcryptSHA256PasswordHasher()

    raise ValueError("Not found algorithm")


def get_random_alphabet(length=12) -> str:
    ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    return "".join(secrets.choice(ALPHABET) for i in range(length))


def make_password(raw_password, salt=None, algorithm="default") -> str:
    hasher = get_hasher(algorithm)
    if salt is None:
        salt = hasher.generate_salt()

    encoded = hasher.encode(raw_password, salt)
    return encoded


def check_password(password, encoded, preferred="default") -> bool:
    hasher = get_hasher(preferred)
    is_correct = hasher.verify(password, encoded)
    return is_correct


class BasePasswordHasher:
    algorithm = None

    def generate_salt(self):
        return get_random_alphabet(12)

    def encode(self, raw_password, salt):
        raise NotImplementedError()  # TODO: Add error message

    def verify(self, password, encoded):
        raise NotImplementedError()  # TODO: Add error message


class BcryptSHA256PasswordHasher(BasePasswordHasher):
    algorithm = "bcrypt_sha256"
    rounds = 12

    def generate_salt(self):
        return bcrypt.gensalt(self.rounds)

    def encode(self, password, salt):
        password = password.encode("utf-8")
        encoded = bcrypt.hashpw(password, salt)
        return encoded

    def verify(self, password, encoded):
        password = password.encode("utf-8")
        return bcrypt.checkpw(password, encoded)
