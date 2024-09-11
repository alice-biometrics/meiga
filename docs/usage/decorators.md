Use decorators to protect your results and prevent from unexpected exceptions. They always return a `Result` object.

## `to_result`

Use `@to_result` to wrap a function transforming returned value in a `Success` and raised Exceptions in a `Failure`.

```python
from meiga import to_result, Result, Error
class NoSuchKey(Exception): ...
class TypeMismatch(Exception): ...

@to_result
def string_from_key(dictionary: dict, key: str) -> str:
    if key not in dictionary.keys():
        raise NoSuchKey()

    value = dictionary[key]
    if not isinstance(value, str):
        raise TypeMismatch()

    return value

dictionary = {"key1": "value", "key2": 2}
key = "key1"

result: Result[str, Error] = string_from_key(dictionary=dictionary, key=key)
```

## `early_return`

Use `@early_return` decoration in combination with `unwrap_or_return()`.
The `unwrap_or_return` will unwrap the value of the `Result` monad only if it is a success.
Otherwise, this will return a Failure (Result with a failure) when using `@early_return` decorator.

```python
from meiga import early_return, BoolResult, isSuccess

@early_return
def update_user(user_id: UserId, new_name: str) -> BoolResult:
     user = repository.retrieve(user_id).unwrap_or_return()
     user.update_name(new_name)
     repository.save(user).unwrap_or_return()
     event_bus.publish(user.pull_domain_events()).unwrap_or_return()
     return isSuccess
```

Given a user repository with a method retrieve which returns a typed `Result[User, UserNotFoundError]`, when we `unwrap_or_return`, we will unwrap the value of returned Result in case of Success.
On the other side, when retrieve function with not valid `UserId`, the repository automatically returns a result failure interrupting the execution of the following lines of code.

!!! note

    This is possible because the `unwrap_or_return` function will raise an specific exception (`OnFailureException`) if the result is a failure an cannot be wrapped:

    ```python
    def unwrap_or_return(self, return_value_on_failure: Any = None) -> TS:
        if not self._is_success:
            return_value = (
                self if return_value_on_failure is None else return_value_on_failure
            )
            raise OnFailureException(return_value)
        return cast(TS, self.value)
    ```

    And `@early_return` decorator catches the exception and coverts it to a `Result`:

    ```python
    P = ParamSpec("P")
    R = TypeVar("R", bound=Result)


    def early_return(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def _early_return(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                if isinstance(func, staticmethod):
                    return Failure(UnexpectedDecorationOrderError())
                elif isinstance(func, classmethod):
                    return Failure(UnexpectedDecorationOrderError())
                else:
                    return func(*args, **kwargs)
            except OnFailureException as exc:
                return exc.result
            except Error as error:
                return cast(R, Failure(error))

        return _early_return
    ```


!!! warning

    When decorate `staticmethod` and `classmethod` check the order, otherwise it will raise an error (UnexpectedDecorationOrderError) as these kinds of methods are not callable.

    ```python
    from meiga import early_return

    class UserCreatorFactory:

        @staticmethod
        @early_return
        def from_version(version: str) -> Result[UserCreator, Error]:
            if version == "migration_v1":
                creator = UserCreator.build()
            else:
                creator = LegacyUserCreator.build()
            return Success(creator)
    ```

## `async_early_return`

Use `@async_early_return` decoration in combination with `unwrap_or_return()` when using async functions.


```python
from meiga import async_early_return, BoolResult, isSuccess

@async_early_return
async def update_user(user_id: UserId, new_name: str) -> BoolResult:
     user = (await repository.retrieve(user_id)).unwrap_or_return()
     user.update_name(new_name)
     (await repository.save(user)).unwrap_or_return()
     (await event_bus.publish(user.pull_domain_events())).unwrap_or_return()
     return isSuccess
```
