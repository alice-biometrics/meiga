This package provides a new type class, the `Result[Type, Type]`.
This Result type allows to simplify a wide range of problems, like handling potential undefined values, or reduce complexity handling exceptions.
Additionally, your code can be simplified following a semantic pipeline reducing the visual noise of checking data types, controlling runtime flow and reducing side effects.

!!! note
    This package is based in another solutions from another modern languages as this Swift-based [Result](https://github.com/antitypical/Result) implementation.


The best way to illustrate how `meiga` can help you, is with some examples.

### Basic Example

Consider the following example of a function that tries to extract a string (`str`) for a given key from a `dict`.

```python
from meiga import Result, Error

class NoSuchKey(Error): ...
class TypeMismatch(Error): ...

def string_from_key(dictionary: dict, key: str) -> Result[str, Error]:
    if key not in dictionary.keys():
        return Result(failure=NoSuchKey())

    value = dictionary[key]
    if not isinstance(value, str):
        return Result(failure=TypeMismatch())

    return Result(success=value)
```

!!! tip "Use alias (Success & Failure) to improve the expressivity of our code"

    ```python hl_lines="8 12 14"
    from meiga import Result, Error

    class NoSuchKey(Error): ...
    class TypeMismatch(Error): ...

    def string_from_key(dictionary: dict, key: str) -> Result[str, Error]:
        if key not in dictionary.keys():
            return Failure(NoSuchKey()) # (1)

        value = dictionary[key]
        if not isinstance(value, str):
            return Failure(TypeMismatch()) # (2)

        return Success(value) # (3)
    ```

    1. Equivalent to use `Result(failure=NoSuchKey())`
    2. Equivalent to use `Result(failure=TypeMismatch())`
    3. Equivalent to use `Result(success=value)`

    See [Alias documentation](usage/alias.md).



Returned `Result` type provides a robust wrapper around the functions and methods. Rather than throw an exception, it returns a `Result` that either contains the success `str` value for the given key, or a typed failure with a specific and detailed `Error` (`Result[str, Error]`).

!!! note
    We can be more specific returning a type as `Result[str, NoSuchKey | TypeMismatch]` or before *PEP 604 (Python 3.10)*, `Result[str, Union[NoSuchKey,TypeMismatch]]`.
    With this type hints we know specifically all result options of our use case.

## Code comparison

In the following examples we compare the same use case using and not using meiga to type the return value.

=== "With meiga 🧙"

    ```python
    from __future__ import annotations
    from meiga import Error, Failure, Result, Success

    class NoSuchKey(Error): ...
    class TypeMismatch(Error): ...

    def string_from_key(
        dictionary: dict, key: str
    ) -> Result[str, NoSuchKey | TypeMismatch]: # 😊 (1)
        if key not in dictionary.keys():
            return Failure(NoSuchKey())

        value = dictionary[key]
        if not isinstance(value, str):
            return Failure(TypeMismatch())

        return Success(value)


    dictionary = {"key1": "value", "key2": 2}
    str_value = string_from_key(dictionary=dictionary, key="key1").unwrap() # 😊 (2)
    ```

    1. This return value is defined with all possible values 🎉.
    2. I'll get a Result (either Success or Failure) and I know possible errors 🎉.

=== "Without meiga 😔"

    ```python hl_lines="17 18 19 20 21 22"
    class NoSuchKey(Exception): ...
    class TypeMismatch(Exception): ...

    def string_from_key(dictionary: dict, key: str) -> str: # 🥲 (1)
        if key not in dictionary.keys():
            raise NoSuchKey()

        value = dictionary[key]
        if not isinstance(value, str):
            raise TypeMismatch()

        return value

    dictionary = {"key1": "value", "key2": 2}
    key = "key1"

    try: # 🥲 (2)
        str_value = string_from_key(dictionary=dictionary, key=key)
    except NoSuchKey:
        print(f"Key {key} does not exist")
    except TypeMismatch:
        print(f"Value of Key {key} is not a string")
    ```

    1.  This return value masks the behavior of the unhappy path (Exceptions). 🥲
        We need to inspect the code to determine what exception might be raised.
    2. Only checking the signature of `string_from_key` method it is imposible to determine which exception should be consider.


## Test comparison

As we can check in the following examples, meiga simplifies our tests with some useful assertion methods.

=== "With meiga 🧙"

    ```python
    import pytest

       from tests.unit.doc.example_without_meiga import (
        NoSuchKey,
        TypeMismatch,
        string_from_key,
    )

    @pytest.mark.unit
    class TestExampleWithMeiga:
        dictionary = {"key1": "value", "key2": 2}

        def should_success(self):
            result = string_from_key(dictionary=self.dictionary, key="key1")
            result.assert_success(value_is_instance_of=str)

        def should_fail_when_key_does_not_exist(self):
            result = string_from_key(dictionary=self.dictionary, key="invalid_key")
            result.assert_failure(value_is_instance_of=NoSuchKey)

        def should_fail_when_type_mismatch(self):
            result = string_from_key(dictionary=self.dictionary, key="key2")
            result.assert_failure(value_is_instance_of=TypeMismatch)
    ```

=== "Without meiga 😔"

    ```python
    import pytest

    from tests.unit.doc.example_without_meiga import (
        NoSuchKey,
        TypeMismatch,
        string_from_key,
    )


    @pytest.mark.unit
    class TestExampleWithoutMeiga:
        dictionary = {"key1": "value", "key2": 2}

        def should_return_a_str(self):
            value = string_from_key(dictionary=self.dictionary, key="key1")
            assert isinstance(value, str)

        def should_raises_non_such_key_exception(self):
            with pytest.raises(NoSuchKey):
                _ = string_from_key(dictionary=self.dictionary, key="invalid_key")

        def should_raises_type_mismatch_exception(self):
            with pytest.raises(TypeMismatch):
                value = string_from_key(dictionary=self.dictionary, key="key2")
                assert not isinstance(value, str)
    ```
