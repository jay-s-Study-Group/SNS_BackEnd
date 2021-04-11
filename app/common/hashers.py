import secrets


def get_random_alphabet(length=12) -> str:
    ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    return "".join(secrets.choice(ALPHABET) for i in range(length))


class BasePasswordHasher:
    algorithm = None

    def generate_salt(self):
        return get_random_alphabet(12)

    def encode(self, raw_password, salt):
        raise NotImplementedError()  # TODO: Add error message

    def verify(self, password, encoded):
        raise NotImplementedError()  # TODO: Add error message
