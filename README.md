meiga
=====

A simple, typed and monad-based Result type for Python.

This package provides a new type for your Python applications, the Result[Type, Type].
This Result type allows to define two subtypes, giving us the option to create useful return types.

This package is based in another solutions from another modern languages as the swift-based [Result](https://github.com/antitypical/Result) implementation.

#### Installation 

~~~
pip install meiga
~~~

#### Getting Started

**meiga** is a framework that give us a simpler, clearer way of handling errors in Python. Use it whenever a class method or a function has the possibility of failure. 

Consider the following example of a function that tries to extract a String (str) for a given key from a Dict.

```python
from meiga import Result, Error


class NoSuchKey(Error):
    pass


class TypeMismatch(Error):
    pass


def string_from_key(dictionary: dict, key: str) -> Result[str, Error]:
    if key not in dictionary.keys():
        return Result(failure=NoSuchKey())

    value = dictionary[key]
    if not isinstance(value, str):
        return Result(failure=TypeMismatch())

    return Result(success=value)
```

Result meiga type provides a robust wrapper around the functions.
Rather than throw an exception, it returns a Result that either contains the String value for the given key, or an ErrorClass detailing what went wrong.

#### Result Type

Let's image we have a dictionary that represent a user info data

```console
>>> user_info = {"first_name": "Rosalia", "last_name": "De Castro", "age": 60}
```

And we try to obtain **first_name** 

```console
>>> result = string_from_key(dictionary=user_info, key="first_name")
Result[status: success | value: Rosalia]
```

You can check the status of the result

```console
>>> result.is_success
True
>>> result.is_failure
False
```

If the result is a success you can get the expected value

```console
>>> result.value
Rosalia 
```

Otherwise, if we try to access an invalid key or a non string value, returned result will be a failure.

```console
>>> result = string_from_key(dictionary=user_info, key="invalid_key")
Result[status: failure | value: NoSuchKey]
>>> result.is_failure
True
>>> result.value
NoSuchKey() // Error 
```

Or

```console
>>> result = string_from_key(dictionary=user_info, key="age")
Result[status: failure | value: TypeMismatch]
>>> result.is_failure
True
>>> result.value
TypeMismatch() // Error 
```

### Alias

Use meiga aliases to improve the semantics of your code.

For success result you can use:

```python
result = Result(success=True)
result = Success()
result = Success(True)
result = isSuccess // Only valid for a success result with a True boolean value
```

For failure results:

```python
result = Result(failure=Error())
result = Failure()
result = Failure(Error())
result = isFailure // Only valid for a failure result with a Error() value
```

You can use this alias with any type

```python
result = Success("user_id")

class UserNotFound(Error):
    pass
result = Failure(UserNotFound())
```

Furthermore, there is a available a useful alias: ```NotImplementedMethodError```

Use it when define abstract method that returns Result type

```python
from meiga import Result, Error, NotImplementedMethodError

from abc import ABCMeta, abstractmethod

class AuthService:

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def create_token(self, client: str, client_id: str) -> Result[str, Error]:
        return NotImplementedMethodError
```


### Handle Result

This framework also allows a method for handling Result type

When the operations is executed with its happy path, handle function returns the success value, as with result.value.

```console
>>> result = string_from_key(dictionary=user_info, key="first_name")
Result[status: success | value: Rosalia]
>>> first_name = result.handle()
Rosalia
```

On the other hand, if something wrong happens handle function will raise an Exception (ReturnErrorOnFailure)

Additionally, handle a Result with the meiga decorator allows to return a typed error when a sub-function fails.

```python
from meiga import Result, Error
from meiga.decorators import meiga

@meiga
def handling_result(key: str) -> Result:
    user_info = {"first_name": "Rosalia", "last_name": "De Castro", "age": 60}
    first_name = string_from_key(dictionary=user_info, key=key).handle() 
    # Do whatever with the name
    name = first_name.lower()
    return Result(success=name)
```

If key is valid success value would be returned. Otherwise, an Error would be returned.


## Developers

##### Install requirements

```console
pip install -r requirements/dev.txt
```

##### Test

```console
pip install -e . && pytest
```

##### Upload to PyPi 

```console
python setup.py sdist bdist_wheel
twine check dist/*
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

