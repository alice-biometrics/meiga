from __future__ import annotations

from timeit import default_number, timeit

from meiga import Error, Failure, Result, Success


class NoSuchKey(Error):
    ...


class TypeMismatch(Error):
    ...


def string_from_key(
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

time_success = timeit(lambda: string_from_key(dictionary=dictionary, key="key1"))
print(f"time when success: {(time_success/default_number)*1000000000} ns")

time_failure_no_such_key = timeit(
    lambda: string_from_key(dictionary=dictionary, key="invalid_key")
)
print(
    f"time when failure (no such key): {(time_failure_no_such_key/default_number)*1000000000} ns"
)

time_failure_type_missmatch = timeit(
    lambda: string_from_key(dictionary=dictionary, key="key2")
)
print(
    f"time when failure (type missmatch): {(time_failure_type_missmatch/default_number)*1000000000} ns"
)
