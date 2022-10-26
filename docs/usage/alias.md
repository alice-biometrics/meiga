Use meiga aliases to improve the semantics of your code. Check out the meiga available alias:

| Alias                        | Definition                                                                  | 
|------------------------------|:----------------------------------------------------------------------------| 
| `Success(value)`             | Equivalent to `Result(success=value)`                                       | 
| `Failure(value)`             | Equivalent to `Result(failure=error_instance)`                              | 
| `isSuccess`                  | Equivalent to `Result(success=True)`                                        |
| `isFailure`                  | Equivalent to `Result(failure=Error())`                                     |
| `NotImplementedMethodError`  | Useful to define abstract methods on interfaces given semantic to your code | 
| `BoolResult`                 | Equivalent to `Result[bool, Error]`                                         |  
| `AnyResult`                  | Equivalent to `Result[Any, Error]`                                          |  

## Success

For success result you can use:

```python
from meiga import Success

result = Success("Rosalia") # the equivalent of Result(success="Rosalia")
```

If you want to return a true bool value, you can use the following equivalent expressions:

```python
from meiga import Success, isSuccess

result = Success()
result = Success(True)
result = isSuccess
``` 

## Failure

For failure results:

```python
from meiga import Failure, Error

class NoSuchKey(Error): ...

result = Failure(NoSuchKey()) # the equivalent of Result(failure=NoSuchKey())
``` 

If you don't want to specify the error, you can use a default value with the following equivalent expressions:

```python
from meiga import Failure, Error, isFailure

result = Failure()
result = Failure(Error())
result = isFailure # Only valid for a failure result with non-specific Error() value
```

???+ Example

    If we review the previous example back [Getting Started](../getting_started.md). We were using already the alias to improve the expressivity of our code:
    
    ```python
    from __future__ import annotations
    from meiga import Result, Error, Success, Failure
    
    class NoSuchKey(Error): ...
    class TypeMismatch(Error): ...
    
    def string_from_key(dictionary: dict, key: str) -> Result[str, NoSuchKey | TypeMismatch]:
        if key not in dictionary.keys():
            return Failure(NoSuchKey())
    
        value = dictionary[key]
        if not isinstance(value, str):
            return Failure(TypeMismatch())
    
        return Success(value)
    ```

## NotImplementedMethodError

Furthermore, there is an available a useful alias: ```NotImplementedMethodError```

Use it when define abstract method that returns Result type

```python
from meiga import Result, Error, NotImplementedMethodError

from abc import ABC, abstractmethod

class AuthService(ABC):

    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def create_token(self, client: str, client_id: str) -> Result[str, Error]:
        return NotImplementedMethodError
```

