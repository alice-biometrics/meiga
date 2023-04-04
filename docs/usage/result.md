`Result[T, Error]` 👉 A discriminated union that encapsulates successful outcome with a value of type T or a failure with an arbitrary Error exception.

## Functions

| Functions                                       | Definition                                                                                                                              |
|-------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------|
| `reraise()` or `throw()`                        | Throws the encapsulated failure value if this instance derive from Error or BaseException.                                              |
| `unwrap()`                                      | Returns the encapsulated value if this instance is a success or None if it is failure.                                                  |
| `unwrap_or_raise()` or `unwrap_or_throw()`      | Returns the encapsulated value if this instance is a success or raise the encapsulated exception if it is failure.                      |
| `unwrap_or_return()`                            | Returns the encapsulated value if this instance is a success or return Result as long as `@early_return` decorator wraps the function.  |
| `unwrap_or(failure_value)`                      | Returns the encapsulated value if this instance is a success or the selected `failure_value` if it is failure.                          |
| `map(transform)`                                | Returns a transformed result applying `transform` function applied to encapsulated value if this instance represents success or failure |
| `unwrap_or_else(on_failure_handler)`            | Returns the encapsulated value if this instance is a success or execute the `on_failure_handler` when it is failure.                    |
| `unwrap_and(on_success_handler)`                | Returns the encapsulated value if this instance is a success and execute the `on_success_handler` when it is success.                   |
| `handle(on_success_handler,on_failure_handler)` | Returns itself and execute the `on_success_handler` when the instance is a success and the `on_failure_handler` when it is failure.     |


## Properties

| Properties      | Definition                                                     |
| --------------- |:--------------------------------------------------------------|
| `value`         | Returns the encapsulated value whether it's success or failure |
| `is_success`    | Returns true if this instance represents successful outcome. In this case is_failure returns false.|
| `is_failure`    | Returns true if this instance represents failed outcome. In this case is_success returns false     |


## Introduction

Let's imagine we have a dictionary that represent a user info data and we use the `string_from_key` (presented in the [Getting Started](../getting_started.md) section before) to retrieve the first name of the user.

```python
user_info = {"first_name": "Rosalia", "last_name": "De Castro", "age": 60}
result = string_from_key(dictionary=user_info, key="first_name")
# ➡ Result will be Result[status: success | value: Rosalia]
```

You could also check the status of the result

```python
is_success = result.is_success
# ➡️ It will return True
is_failure = result.is_failure
# ➡️ It will return False
```

If the result is a success you can get the expected value accessing the property `value` or using the `unwrap` function (recommended).

```python
my_value = result.value
# ➡️ It will return Rosalia
my_value = result.unwrap()
# ➡️ It will return also Rosalia
```

Otherwise, if we try to access an invalid key or a non string value, returned result will be a failure.

```python
result = string_from_key(dictionary=user_info, key="invalid_key")
# ➡ Result will be Result[status: failure | value: NoSuchKey]
is_success = result.is_success
# ➡️ It will return False
is_failure = result.is_failure
# ➡️ It will return True
my_value = result.value
# ➡️ It will return NoSuchKey (Error)
my_value = result.unwrap()
# ➡️ It will return also NoSuchKey (Error)
```

Or

```python
result = string_from_key(dictionary=user_info, key="age")
# ➡ Result will be Result[status: failure | value: TypeMismatch]
is_success = result.is_success
# ➡️ It will return False
is_failure = result.is_failure
# ➡️ It will return True
my_value = result.value
# ➡️ It will return TypeMismatch (Error)
my_value = result.unwrap()
# ➡️ It will return also TypeMismatch (Error)
```
