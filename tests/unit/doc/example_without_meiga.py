class NoSuchKey(Exception):
    ...


class TypeMismatch(Exception):
    ...


# This return value masks the behavior of the unhappy path (Exceptions). 🥲
# We need to inspect the code to determine what exception might be raised.
def string_from_key(dictionary: dict, key: str) -> str:
    if key not in dictionary.keys():
        raise NoSuchKey()

    value = dictionary[key]
    if not isinstance(value, str):
        raise TypeMismatch()

    return value


dictionary = {"key1": "value", "key2": 2}
key = "key1"

try:
    str_value = string_from_key(dictionary=dictionary, key=key)
except NoSuchKey:
    print(f"Key {key} does not exist")
except TypeMismatch:
    print(f"Value of Key {key} is not a string")
