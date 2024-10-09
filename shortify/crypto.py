import hashlib


ENCODING = "UTF-8"


def sha256(string: str) -> str:
    return hashlib.sha256(string.encode(ENCODING)).hexdigest()
