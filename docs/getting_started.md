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

Returned `Result` type provides a robust wrapper around the functions and methods. Rather than throw an exception, it returns a `Result` that either contains the success `str` value for the given key, or a typed failure with a specific and detailed `Error` (`Result[str, Error]`).

!!! note 
    We can be more specific returning a type as `Result[str, NoSuchKey | TypeMismatch]` or before *PEP 604 (Python 3.10)*, `Result[str, Union[NoSuchKey,TypeMismatch]]`.
    With this type hints we know specifically all result options of our use case.

## Code comparison with and without meiga 

### Without meiga

```python
class NoSuchKey(Exception): ...
class TypeMismatch(Exception): ...

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
```

### With meiga

```python
from __future__ import annotations
from meiga import Error, Failure, Result, Success

class NoSuchKey(Error): ...
class TypeMismatch(Error): ...

# This return value is defined with all possible values 😊
def string_from_key(dictionary: dict, key: str) -> Result[str, NoSuchKey | TypeMismatch]:
    if key not in dictionary.keys():
        return Failure(NoSuchKey())

    value = dictionary[key]
    if not isinstance(value, str):
        return Failure(TypeMismatch())

    return Success(value)


dictionary = {"key1": "value", "key2": 2}
str_value = string_from_key(dictionary=dictionary, key="key1").unwrap()
# 😊 I'll get a Result (either Success or Failure) and I know possible errors
```

## Test comparison with and without meiga 

### Without meiga

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

### With meiga

```python
import pytest

from tests.unit.doc.example_with_meiga import NoSuchKey, TypeMismatch, string_from_key


@pytest.mark.unit
class TestExampleWithMeiga:
    dictionary = {"key1": "value", "key2": 2}

    def should_success(self):
        result = string_from_key(dictionary=self.dictionary, key="key1")
        result.assert_success(result, value_is_instance_of=str)

    def should_fail_when_key_does_not_exist(self):
        result = string_from_key(dictionary=self.dictionary, key="invalid_key")
        result.assert_failure(result, value_is_instance_of=NoSuchKey)

    def should_fail_when_type_mismatch(self):
        result = string_from_key(dictionary=self.dictionary, key="key2")
        result.assert_failure(result, value_is_instance_of=TypeMismatch)

```


!!! note
    Check out everything that can be done with the `Result` type in the next section (Result Type). 