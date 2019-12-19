meiga 🧙 [![ci](https://github.com/alice-biometrics/meiga/workflows/ci/badge.svg)](https://github.com/alice-biometrics/meiga/actions)  [![ci](https://github.com/alice-biometrics/meiga/workflows/pypi/badge.svg)](https://github.com/alice-biometrics/meiga/actions) [![pypi](https://img.shields.io/pypi/dm/meiga)](https://pypi.org/project/meiga/)
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
result = Result(success="Rosalia")
result = Success("Rosalia") # bool value
```

If return value is a bool you can use:

```python
result = Success()
result = Success(True)
result = isSuccess
``` 

For failure results:

```python
class NoSuchKey(Error):
    pass

result = Result(failure=NoSuchKey())
result = Failure(NoSuchKey())
``` 

If you don't want to specify the error, you can use default value with:

```python
result = Failure()
result = Failure(Error())
result = isFailure # Only valid for a failure result with a Error() value
```

Bringing previous example back. that is the way you can use the alias:

```python
from meiga import Result, Error, Success, Failure,


class NoSuchKey(Error):
    pass


class TypeMismatch(Error):
    pass


def string_from_key(dictionary: dict, key: str) -> Result[str, Error]:
    if key not in dictionary.keys():
        return Failure(NoSuchKey())

    value = dictionary[key]
    if not isinstance(value, str):
        return Failure(TypeMismatch())

    return Success(value)
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

In addition, you can call another function after evaluate the result. Use optional parameters **success_handler** and **failure_handler** (Callable functions).

```python
def success_handler():
    print("Do my successful stuff here!")

def failure_handler():
     print("Do my failure stuff here!")


result = string_from_key(dictionary=user_info, key="first_name")

result.handle(success_handler=success_handler, failure_handler=failure_handler)
```

If you need to add some arguments as a parameters, use **success_args** and **failure_args**:

```python
def success_handler(param_1):
    print(f"param_1: {param_1}")

def failure_handler(param_1, param_2):
    print(f"param_1: {param_1}")
    print(f"param_2: {param_2}")


result = string_from_key(dictionary=user_info, key="first_name")

result.handle(success_handler=success_handler, 
              failure_handler=failure_handler,
              success_args=1,
              failure_args=(1, 2))
```


On the other hand, if something wrong happens handle function will raise an Exception (ReturnErrorOnFailure). 
Meiga has available a decorator to allow to handle the exception in case of error and unwrap the value in case of success.


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


### Assertions

To help us on testing functions that returns Result, meiga provide us two functions: **assert_success** and **access_failure**.

Check the following pytest-based test: [tests/unit/test_result_assertions.py](https://github.com/alice-biometrics/meiga/blob/master/tests/unit/test_result_assertions.py)


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

