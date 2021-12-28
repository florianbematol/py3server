# py3server

py3server is a web application framework, based on decorators patterns.

# Documentation

You can find package API documentation [here](docs/README.md).

# Installing

Install and update using pip:

```shell
    $ pip install -U py3server
```

# Example

```python
# main.py
from py3server.booter import Booter


def main():
    """ """
    Booter(__file__).run()


if __name__ == '__main__':
    main()
```

```python
# user_controller.py
from py3server.web.controllers.rest_controller import RestController
from py3server.web.mapping.post_mapping import PostMapping
from py3server.web.params.body import Body
from py3server.web.response import Response
from .user_service import UserService


@RestController('/users')
class UserController():
    user_service: UserService

    @PostMapping()
    def create_user(self, body: Body):
        user = self.user_service.add_user(body)
        return Response(200, user)
```

```python
# user_service.py
from py3server.app.service import Service
from .user_repository import UserRepo


@Service()
class UserService():
    user_repo: UserRepo

    def add_user(self, data):
        firstname = data["firstname"]
        lastname = data["lastname"]
        return self.user_repo.add_user(firstname, lastname)
```

```python
# user_repo.py
from py3server.app.repository import Repository


@Repository()
class UserRepo():
    users = []

    def add_user(self, firstname, lastname):
        user = {
            "firstname": firstname,
            "lastname": lastname
        }
        self.users.append(user)
        return user
```