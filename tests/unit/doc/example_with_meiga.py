from typing import Union

from meiga import Error, Failure, Result, Success


class NoSuchKey(Error):
    ...


class TypeMismatch(Error):
    ...


def string_from_key(
    dictionary: dict, key: str
) -> Result[str, Union[NoSuchKey, TypeMismatch]]:
    if key not in dictionary.keys():
        return Failure(NoSuchKey())

    value = dictionary[key]
    if not isinstance(value, str):
        return Failure(TypeMismatch())

    return Success(value)


dictionary = {"key1": "value", "key2": 2}
str_value = string_from_key(dictionary=dictionary, key="key1").unwrap()
# 😊 I'll get a Result (either Success or Failure) and I know possible errors
