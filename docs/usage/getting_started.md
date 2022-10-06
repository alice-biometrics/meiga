This package provides a new type class, the `Result[Type, Type]`
This Result type allows to simplify a wide range of problems, like handling potential undefined values, or reduce complexity handling exceptions. Additionally, code can be simplified following a semantic pipeline reducing the visual noise of checking data types, controlling runtime flow and side-effects.

This package is based in another solutions from another modern languages as this swift-based [Result](https://github.com/antitypical/Result) implementation.

### Example

The best way to illustrate how `meiga` can help you is with an example.

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

Returned `Result` type provides a robust wrapper around the functions and methods. Rather than throw an exception, it returns a `Result` that either contains the `str` value for the given key, or an typed `Error`  detailing what went wrong (`Result[str, Error]`).

You can be more specific returning a type  `Result[str, NoSuchKey | TypeMismatch]` or before *PEP 604 (Python 3.10)*, `Result[str, Union[NoSuchKey,TypeMismatch]]` 

Check out everything that can be done with the `Result` type in the next section (Result Type). 