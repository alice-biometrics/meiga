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

~~~
>>> user_info = {"first_name": "Rosalia", "last_name": "De Castro", "age": 60}
~~~

And we try to obtain **first_name** 

~~~
>>> result = string_from_key(dictionary=user_info, key="first_name")
Result[status: success | value: Rosalia]
~~~

You can check the status of the result

~~~
>>> result.is_success
True
>>> result.is_failure
False
~~~

If the result is a success you can get the expected value

~~~
>>> result.value
Rosalia 
~~~

Otherwise, if we try to access an invalid key or a non string value, returned result will be a failure.

~~~
>>> result = string_from_key(dictionary=user_info, key="invalid_key")
Result[status: failure | value: NoSuchKey]
>>> result.is_failure
True
>>> result.value
NoSuchKey() // Error 
~~~

Or

~~~
>>> result = string_from_key(dictionary=user_info, key="age")
Result[status: failure | value: TypeMismatch]
>>> result.is_failure
True
>>> result.value
TypeMismatch() // Error 
~~~

# Handle Result

This framework also allows a method for handling Result type

When the operations is executed with its happy path, handle function returns the success value, as with result.value.

~~~
>>> result = string_from_key(dictionary=user_info, key="first_name")
Result[status: success | value: Rosalia]
>>> first_name = result.handle()
Rosalia
~~~

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

~~~
pip install -r requirements/dev.txt
~~~

##### Test

~~~
pip install -e . && pytest
~~~

##### Upload to PyPi 

~~~
python setup.py sdist bdist_wheel
twine check dist/*
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
~~~
