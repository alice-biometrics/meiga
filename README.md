meiga (beta)
============

A simple, typed and monad-based Result type for Python.

#### Installation 

~~~
pip install meiga
~~~

#### Getting Started

**meiga** is a framework that give us a simpler, clearer way of handling errors in Python. 

~~~
from meiga import Result

def is_positive(num: int) -> Result[bool, Error]:
    if num < 0:
        return Result(failure=Error())    
    return Result(success=True)
~~~

Result object can be initialized as a success or failure. Additionally, it can be typed.

Let's present it within a real use case to show how useful can be:

Imagine you have a Repository of your Domain Entity User, and it allow you to save an instance of an User.

You can use a standard way raising Exceptions
~~~
class UserRepository:

    def save(user: User) -> bool:
        try:
            orm.save(user)
        except OrmConnectionException, OrmBusyException as e:
            raise e
~~~

Or, you can model the problem in a different way using a Result

~~~
from meiga import Result, Error

class DatabaseConnectionError(Error):
    pass

class DatabaseBusyError(Error):
    pass

class UserRepository:

    def save(user: User) -> Result[bool, Error]:
        try:
            orm.save(user)
        except OrmConnectionException:
            return Result(failure=DatabaseConnectionError())
        except OrmBusyException:
            return Result(failure=DatabaseBusyError())
~~~

Until now, both strategies seams quite similar. However, how do we deal with these options?
Imagine, we are developing the CreateUser Use Case. 


*Standard way*
~~~
class CreateUser(UseCase):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str):
        try:
            user = User(email=email)
            self.user_repository.save()
        except Exception as e:
            raise e
~~~

*meiga way*
~~~
from meiga import Result, Error
from meiga.decorators import meiga, return_on_failure

class CreateUser(UseCase):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @meiga 
    def execute(self, email: str) -> Result[bool, Error]:
        self.user_repository.save(user=User(email=email)).handle()
        return Result(success=True)
~~~
