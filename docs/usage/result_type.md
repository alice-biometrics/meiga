`Result[T, Error]` 👉 A discriminated union that encapsulates successful outcome with a value of type T or a failure with an arbitrary Error exception.

## Functions

| Functions                                       | Definition                                                                                                                              | 
|-------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------| 
| `throw()`                                       | Throws the encapsulated failure value if this instance derive from Error or BaseException.                                              | 
| `unwrap()`                                      | Returns the encapsulated value if this instance is a success or None if it is failure.                                                  | 
| `unwrap_or_throw()`                             | Returns the encapsulated value if this instance is a success or throws the encapsulated exception if it is failure.                     |  
| `unwrap_or_return()`                            | Returns the encapsulated value if this instance is a success or return Result as long as `@meiga` decorator wraps the function.         |  
| `unwrap_or(failure_value)`                      | Returns the encapsulated value if this instance is a success or the selected `failure_value` if it is failure.                          |  
| `unwrap_or_else(on_failure_handler)`            | Returns the encapsulated value if this instance is a success or execute the `on_failure_handler` when it is failure.                    |   
| `unwrap_and(on_success_handler)`                | Returns the encapsulated value if this instance is a success and execute the `on_success_handler` when it is success.                   |   
| `handle(on_success_handler,on_failure_handler)` | Returns itself and execute the `on_success_handler` when the instance is a success and the `on_failure_handler` when it is failure.     |  
| `map(transform)`                                | Returns a transformed result applying `transform` function applied to encapsulated value if this instance represents success or failure | 


## Properties

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
    first_name = string_from_key(dictionary=user_info, key=key).unwrap_or_return() 
    # Do whatever with the name
    name = first_name.lower()
    return Result(success=name)
```

If key is valid success value would be returned. Otherwise, an Error would be returned.

If you need to return a specific value if fails, you can do it with meiga:

```python
first_name = string_from_key(dictionary=user_info, key=key).unwrap_or_return(return_value_on_failure=isSuccess) 
```

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

##### Additional parameters

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

##### Additional parameters in combination with the Result itself

Sometimes a handle function will need information about external parameters and also about the result itself. Now, is possible this combination thanks to `Result.__id__` identifier.

```python
from meiga import Result, Error, OnSuccessHandler, OnFailureHandler
from meiga.decorators import meiga

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


@meiga
def run(result: Result):
    result.handle(
        on_success_handler=OnSuccessHandler(func=success_handler, args=args),
        on_failure_handler=OnFailureHandler(func=failure_handler, args=args)
    )

run(result)
```
