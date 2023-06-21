from __future__ import annotations

import pyperf

from meiga import Error, Failure, Result, Success


# Without meiga
class NoSuchKeyException(Exception):
    ...


class TypeMismatchException(Exception):
    ...


def string_from_key(dictionary: dict, key: str) -> str:
    if key not in dictionary.keys():
        raise NoSuchKeyException()

    value = dictionary[key]
    if not isinstance(value, str):
        raise TypeMismatchException()

    return value


def string_from_key_without_meiga(dictionary: dict, key: str) -> str:
    try:
        return string_from_key(dictionary, key)
    except Exception:  # noqa
        pass


# With meiga
class NoSuchKey(Error):
    ...


class TypeMismatch(Error):
    ...


def string_from_key_with_meiga(
    dictionary: dict, key: str
) -> Result[str, NoSuchKey | TypeMismatch]:
    if key not in dictionary.keys():
        return Failure(NoSuchKey())

    value = dictionary[key]
    if not isinstance(value, str):
        return Failure(TypeMismatch())

    return Success(value)


dictionary = {
    "key1": "value",
    "key2": 2,
    "key3": "value",
    "key4": 2,
    "key5": "value",
    "key6": 2,
    "key7": "value",
    "key8": 2,
    "key9": "value",
    "key10": 2,
    "key11": "value",
    "key12": 2,
}


def meiga():
    string_from_key_with_meiga(dictionary=dictionary, key="invalid_key")


def without_meiga():
    string_from_key_without_meiga(dictionary=dictionary, key="invalid_key")


runner = pyperf.Runner()
runner.bench_func("meiga", meiga)
runner.bench_func("without meiga", without_meiga)
