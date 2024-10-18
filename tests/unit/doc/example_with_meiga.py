from __future__ import annotations

from meiga import Error, Failure, Result, Success


class NoSuchKey(Error):
    ...


class TypeMismatch(Error):
    ...


def string_from_key(dictionary: dict, key: str) -> Result[str, NoSuchKey | TypeMismatch]:
    if key not in dictionary.keys():
        return Failure(NoSuchKey())

    value = dictionary[key]
    if not isinstance(value, str):
        return Failure(TypeMismatch())

    return Success(value)


dictionary = {"key1": "value", "key2": 2}
result = string_from_key(dictionary=dictionary, key="key1")
# 😊 I'll get a Result (either Success or Failure) and I know possible errors
