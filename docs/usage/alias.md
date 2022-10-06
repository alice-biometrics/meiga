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
class NoSuchKey(Error): ...

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

class NoSuchKey(Error): ...
class TypeMismatch(Error): ...

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

from abc import ABC, abstractmethod

class AuthService(ABC):

    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def create_token(self, client: str, client_id: str) -> Result[str, Error]:
        return NotImplementedMethodError
```