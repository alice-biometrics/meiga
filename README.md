# meiga 🧙 [![version](https://img.shields.io/github/release/alice-biometrics/meiga/all.svg)](https://github.com/alice-biometrics/meiga/releases) [![ci](https://github.com/alice-biometrics/meiga/workflows/ci/badge.svg)](https://github.com/alice-biometrics/meiga/actions) [![pypi](https://img.shields.io/pypi/dm/meiga)](https://pypi.org/project/meiga/)

<img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/alice_header.png" width=auto>

A simple, typed and monad-based Result type for Python. 

## Table of Contents
- [Installation :computer:](#installation-computer)
- [Getting Started :chart_with_upwards_trend:](#getting-started-chart_with_upwards_trend)
  * [Example](#example)
  * [Features](#features)
    - [Result](#result)
    - [Functions](#functions)
    - [Properties](#properties)
    - [Alias](#alias)
- [Advance Usage :rocket:](#advance-usage-rocket)
  * [Unwrap Result](#unwrap-result)
  * [Handle Result](#handle-result)
  * [Test Assertions](#test-assertions)
- [Contact :mailbox_with_mail:](#contact-mailbox_with_mail)


## Installation :computer:

~~~
pip install meiga
~~~

## Getting Started :chart_with_upwards_trend:	

**Meiga** give us a simpler and clearer way of handling errors in Python. Use it whenever a class method or a function has the possibility of failure. 

This package provides a new type for your Python applications, the **Result[Type, Type]**.
This Result type allows to simplify a wide range of problems, like handling potential undefined values, or reduce complexity handling exceptions. Additionally, code can be simplified following a semantic pipeline reducing the visual noise of checking data types, controlling runtime flow and side-effects.

This package is based in another solutions from another modern languages as the swift-based [Result](https://github.com/antitypical/Result) implementation.

### Example

The best way to illustrate how **meiga 🧙** can help you is with an example.

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

### Features

#### Result

`Result[T, Error]` 👉 A discriminated union that encapsulates successful outcome with a value of type T or a failure with an arbitrary Error exception.

#### Functions

| Functions                       | Definition                                                                                   | 
| --------------------------------|:-------------------------------------------------------------------------------------------- | 
| `throw()`                       | Throws the encapsulated failure value if this instance derive from Error or BaseException.    | 
| `unwrap()`                      | Returns the encapsulated value if this instance represents success or None if it is failure. | 
| `unwrap_or_throw()`             | Returns the encapsulated value if this instance represents success or throws the encapsulated exception if it is failure. |  
| `unwrap_or_return()`            | Returns the encapsulated value if this instance represents success or return Result as long as `@meiga` decorator wraps the function |  
| `unwrap_or(failure_value)`      | Returns the encapsulated value if this instance represents success or the selected `failure_value` if it is failure. |  
| `unwrap_or_else(on_failure)`    | Returns the encapsulated value if this instance represents success or execute the `on_failure` function when it is failure. |   
| `unwrap_and(on_success)`        | Returns the encapsulated value if this instance represents success and execute the `on_success` function when it is success. |   
| `handle(on_success,on_failure)` | Returns itself and execute the `on_success`function when the instance represemts success and the `on_failure` function when it is failure. |  
| `map(transform)`                | Returns a transformed result applying `transform` function applied to encapsulated value if this instance represents success or failure | 


#### Properties

| Properties      | Definition                                                     | 
| --------------- |:--------------------------------------------------------------| 
| `value`         | Returns the encapsulated value whether it's success or failure | 
| `is_success`    | Returns true if this instance represents successful outcome. In this case is_failure returns false.|   
| `is_failure`    | Returns true if this instance represents failed outcome. In this case is_success returns false     | 


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

#### Alias

Use meiga aliases to improve the semantics of your code.

For success result you can use:

```python
result = Result(success="Rosalia")
result = Success("Rosalia") # it is equivalent
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
result = isFailure # Only valid for a failure result with non-specific Error() value
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

## Advance Usage :rocket:

### Unwrap Result

If you *wrap* a Result object, its will return a valid value if it is success. Otherwise, it will return None.

```python
result = Result(success="Hi!")
value = result.unwrap()
assert value == "Hi!"

result = Failure(Error())
value = result.unwrap()

assert value is None
```

* Check [Functions](#functions) to know more about *unwraping* methods.
* Check [tests/unit/test_result_unwrap.py](https://github.com/alice-biometrics/meiga/blob/master/tests/unit/test_result_unwrap.py) to see examples of usage.


You can use `unwrap_or_return`in combination with `@meiga` decorator. If something wrong happens unwraping your `Result`, the `unwrap_or_return` function will raise an Exception (ReturnErrorOnFailure). `@meiga` decorator allows to handle the exception in case of error and unwrap the value in case of success. The following example illustrate this:

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


### Handle Result

This framework also allows a method for handling Result type. `handle` method returns itself and execute the `on_success` function when the instance represemts success and the `on_failure` function when it is failure.


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

result.handle(on_success=success_handler, on_failure=failure_handler)
```

##### Additional parameters

If you need to add some arguments as a parameters, use **success_args** and **failure_args**:

```python
def success_handler(param_1):
    print(f"param_1: {param_1}")

def failure_handler(param_1, param_2):
    print(f"param_1: {param_1}")
    print(f"param_2: {param_2}")


result = string_from_key(dictionary=user_info, key="first_name")

result.handle(on_success=success_handler, 
              on_failure=failure_handler,
              success_args=1,
              failure_args=(1, 2))
```

##### Additional parameters in combination with the Result itself

Sometimes a handle function will need information about external parameters and also about the result itself. Now, is possible this combination thanks to `Result.__id__` identifier. 

```python
    parameters = (1, Result.__id__, 2)

    def on_success(param_1: int, result: Result, param_2: int):
        assert param_1 == 1
        assert isinstance(result, Result)
        assert result.value is True
        assert param_2 == 2

    def on_failure(param_1: int, result: Result, param_2: int):
        assert param_1 == 1
        assert isinstance(result, Result)
        assert result.value == Error()
        assert param_2 == 2

    @meiga
    def run():
        result.handle(
            on_success=on_success,
            on_failure=on_failure,
            success_args=parameters,
            failure_args=parameters,
        )

    run()
```




### Test Assertions

To help us on testing functions that returns Result, meiga provide us two functions: **assert_success** and **access_failure**.

Check the following pytest-based test for more information: [tests/unit/test_result_assertions.py](https://github.com/alice-biometrics/meiga/blob/master/tests/unit/test_result_assertions.py)

## Contact :mailbox_with_mail:

support@alicebiometrics.com
