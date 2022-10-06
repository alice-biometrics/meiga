Use `@meiga` as a decorator to protect your results and prevent from unexpected exceptions. It always returns a `Result` object.

```python
from meiga.decorators import meiga

@meiga
def create_user(user_id: UserId) -> BoolResult:
     user = user_creator.execute(user_id).unwrap_or_return()
     return repository.save(user)
```     

When decorate `staticmethod` and `classmethod` check the order, otherwise it will raise an error (UnexpectedDecorationOrderError) as these kinds of methods are not callable

```python
from meiga.decorators import meiga

class UserCreatorFactory:

    @staticmethod
    @meiga
    def from_version(version: str) -> Result[UserCreator, Error]:
        if version == "migration_v1":
            creator = UserCreator.build()
        else:
            creator = LegacyUserCreator.build()
        return Success(creator)
```