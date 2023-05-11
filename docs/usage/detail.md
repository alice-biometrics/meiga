We will present some tips and examples to see in detail what meiga can offer us.

### `throw`

Throws the encapsulated failure value if this instance inherits from Error or BaseException.

???+ example

    ```python
    result = Success("Hi!")
    result.throw() # ➡️ It won't throw an exception as is a success. So, this will return None

    result = Failure(Error())
    result.throw() # ➡️ It will throw an exception using given Error instance
    ```

### `unwrap`

Returns the encapsulated value if this instance is a success or None if it is failure.

???+ example

    If you `unwrap` a Result object, it will return a valid value if it is success. Otherwise, it will return None.

    ```python
    result = Result(success="Hi!")
    value = result.unwrap() # ➡️ It will return "Hi!"

    result = Failure(Error())
    value = result.unwrap() # ➡️ It will return None
    ```

    See [tests/unit/test_result_unwrap.py](https://github.com/alice-biometrics/meiga/blob/master/tests/unit/test_result_unwrap.py) to see examples of usage.


### unwrap_or_throw

Returns the encapsulated value if this instance is a success or throws the encapsulated exception if it is failure.

???+ example

    ```python
    result = Result(success="Hi!")
    value = result.unwrap_or_throw() # ➡️ It will return "Hi!"

    result = Failure(Error())
    value = result.unwrap_or_throw() # ➡️ It will throw an exception using given Error instance
    ```

### `unwrap_or_return`

Returns the encapsulated value if this instance is a success or return Result as long as `@early_return` decorator wraps the function.


???+ example

    Use `unwrap_or_return` in combination with `@early_return` decorator.
    If something wrong happens unwrapping your `Result`, the `unwrap_or_return` function will raise an controlled Exception (ReturnErrorOnFailure).
    `@early_return` decorator will handle the exception and unwrap the value in case of success.
    The following example illustrate this:


    ```python
    from meiga import Result, Error, early_return

    @early_return
    def handling_result(key: str) -> Result:
        user_info = {"first_name": "Rosalia", "last_name": "De Castro", "age": 60}
        first_name = string_from_key(dictionary=user_info, key=key).unwrap_or_return()
        # Do whatever with the name
        name = first_name.lower()
        return Result(success=name)
    ```

    If key is valid success value would be returned. Otherwise, an Error would be returned.

    If you need to return a specific value if fails, you can do it with meiga:

    ```python
    first_name = string_from_key(
        dictionary=user_info,
        key=key
    ).unwrap_or_return(return_value_on_failure=MyError())
    ```

### unwrap_or

Returns the encapsulated value if this instance is a success or the selected failure_value if it is failure.

???+ example

    ```python
     first_name = string_from_key(
        dictionary=user_info,
        key=key
     ).unwrap_or(failure_value="UserWithoutName")
     # It will return the first name if success or "UserWithoutName" if failure
    ```

### map

Returns a transformed result applying transform function applied to encapsulated value if this instance represents success or failure

???+ example

    ```python

    def capitalize(value):
        return value.capitalize()

    first_name = string_from_key(
        dictionary=user_info,
        key=key
    ).map(capitalize)
    ```

### handlers

Ways to handle and react to result.

#### unwrap_or_else

Returns the encapsulated value if this instance is a success or execute the on_failure_handler when it is failure.

???+ example

    ```python
    from meiga import OnFailureHandler

    def on_failure_func():
        print("Do your staff here to react to a failure")

    first_name: str = string_from_key(
        dictionary=user_info,
        key=key
    ).unwrap_or_else(on_failure_handler=OnFailureHandler(func=failure_handler))
    ```

#### unwrap_and

Returns the encapsulated value if this instance is a success and execute the on_success_handler when it is success.

???+ example

    ```python
    from meiga import OnSuccessHandler

    def on_success_func():
        print("Do your staff here to react to a success")

    first_name: str = string_from_key(
        dictionary=user_info,
        key=key
    ).unwrap_and(on_success_handler=OnSuccessHandler(func=on_success_func))
    ```

#### handle

Returns itself and execute the on_success_handler when the instance is a success and the on_failure_handler when it is failure.

???+ example

    You can call another function after evaluate the result.
    Use optional parameters **success_handler** and **failure_handler** (Callable functions).

    ```python
    from meiga import OnSuccessHandler, OnFailureHandler

    def success_handler():
        print("Do my successful stuff here!")


    def failure_handler():
        print("Do my failure stuff here!")


    result = string_from_key(dictionary=user_info, key="first_name")

    result.handle(
        on_success_handler=OnSuccessHandler(func=success_handler),
        on_failure_handler=OnFailureHandler(func=failure_handler)
    )
    ```

??? tip "Tip: Additional parameters"

    If you need to add some arguments as a parameters, use **success_args** and **failure_args**:

    ```python
    from meiga import OnSuccessHandler, OnFailureHandler

    def success_handler(param_1):
        print(f"param_1: {param_1}")

    def failure_handler(param_1, param_2):
        print(f"param_1: {param_1}")
        print(f"param_2: {param_2}")


    result = string_from_key(dictionary=user_info, key="first_name")

    result.handle(
        on_success_handler=OnSuccessHandler(func=success_handler, args=(1,)),
        on_failure_handler=OnFailureHandler(func=failure_handler, args=(1, 2))
    )
    ```

??? tip "Tip: Additional parameters in combination with the Result itself"

    Sometimes a handle function will need information about external parameters and also about the result itself. Now, is possible this combination thanks to `Result.__id__` identifier.

    ```python
    from meiga import Result, Error, OnSuccessHandler, OnFailureHandler

    args = (1, Result.__id__, 2)

    def success_handler(param_1: int, result: Result, param_2: int):
        assert param_1 == 1
        assert isinstance(result, Result)
        assert result.value is True
        assert param_2 == 2


    def failure_handler(param_1: int, result: Result, param_2: int):
        assert param_1 == 1
        assert isinstance(result, Result)
        assert result.value == Error()
        assert param_2 == 2

    def run(result: Result):
        result.handle(
            on_success_handler=OnSuccessHandler(func=success_handler, args=args),
            on_failure_handler=OnFailureHandler(func=failure_handler, args=args)
        )

    run(result)
    ```

#### match

!!! info "Python > 3.10"

    If you are using **Python 3.10 or above**, you can take advantage of new syntax proposed in [PEP 636 – Structural Pattern Matching](https://peps.python.org/pep-0636/)
    to handle the result.

```python hl_lines="27 28 29 30 31 32 33 34 35"
from __future__ import annotations

from meiga import Error, Failure, Result, Success


class NoSuchKey(Error): ...
class TypeMismatch(Error): ...


def string_from_key(
    dictionary: dict, key: str
) -> Result[str, NoSuchKey | TypeMismatch]:
    if key not in dictionary.keys():
        return Failure(NoSuchKey())

    value = dictionary[key]
    if not isinstance(value, str):
        return Failure(TypeMismatch())

    return Success(value)


dictionary = {"key1": "value", "key2": 2}

for key in ["key1", "key2", "key3"]:
    result = string_from_key(dictionary=dictionary, key=key)
    match result:
        case Success(_):
            print(f"Success")
        case Failure(NoSuchKey()):
            print("Failure with NoSuchKey")
        case Failure(TypeMismatch()):
            print("Failure with TypeMismatch")
        case _:
            print("default")
```

!!! Warning

    If are using `Result(success="my_success")` and `Result(failure=NoSuchKey())` syntax intead of recommended one
    with `Success` and `Failure` aliases, you have to use a different match pattern.

    You would have to use something like:

    ```python
    match result:
        case Result(str(), _):
            print(f"Success")
        case Result(_, NoSuchKey()):
            print("Failure with NoSuchKey")
        case Result(_, TypeMismatch()):
            print("Failure with TypeMismatch")
        case _:
            print("default")
    ```

    Check this [closed issue](https://github.com/alice-biometrics/meiga/issues/56) to learn more about the `PEP 636` and this usage in the meiga library.
