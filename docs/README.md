# <span name="documentation">Documentation</span>

## <span name="application">Application</span>

To run your server you need to use the [Booter](#booter) inside a file located at root of your project.

### <span name="booter">Booter(root_file)</span>

Launch your server on port `8080` by default, after discovering and building context.

**Parameters**

* **root_file** (str) - `__name__` of your root file.

**Example**

If I have a project structure like this:

```
project
│   main.py
└───controllers
│   └───users_controller.py
└───services
│   └───users_service.py
└───repositories
    └───users_repository.py
```

Your `main.py` should contain:

```python
from py3server import Booter

Booter.run(__name__)
```

Then when you run:

```shell
$ python main.py
```

Your server will start, discover your components and then listen on port `8080` by default.

<br/>

### <span name="service">@Service</span>

Services class are used to write business logic, separated from [@RestController](#rest-controller) class.

**Parameters**

**Example**

Register an `UserService` class.

```python
from py3server.app import Service


@Service()
class UserService:
    pass
```

<br/>

### <span name="service">@ExceptionHandler(_types_=[Exception])</span>

Used to register a class as an exceptions' handler for `types` exception's.

Decorated class need to have a method `handle_exception(self, exception)`

**Parameters**

* **types** (Exception[]) - List of exception types to match.

**Example**

Register an exception handler for all exceptions.

```python
from py3server.app import ExceptionHandler


@ExceptionHandler()
class DefaultExceptionHandler:
    def handle_exception(self, exception):
        pass
```

<br/>

### <span name="repository">@Repository</span>

Repositories class are used to write storage, retrieval of objects.

**Parameters**

**Example**

Register an `UserRepository` class.

```python
from py3server.app import Repository


@Repository()
class UserRepository:
    pass
```

<br/>

## <span name="routing">Routing</span>

### <span name="rest-controller">@RestController(_url_)</span>

Decorate a class to register it as a **Controller** with the given `url`.

**Parameters**

* **path** (str) - Base url of inside routes.

**Example**

Register an user `/users` controller.

```python
from py3server.web.controllers import RestController


@RestController('/users')
class UserController:
    pass
```

<br/>

### <span name="get-mapping">@GetMapping(_url_, _produces=MediaType.APPLICATION_JSON_)</span>

Decorate a function inside a class decorated with [@RestController](#rest-controller) to register the `url` with rules.

Only `HTTP GET` method will be matching.

The `url` can extract data if it contains `{<id>}` or with regex: `{<id>:<regex>}`.

To access extracted data of the `url` you need to use [PathParam](#path-param).

**Parameters**:

* **path** (str) - Request URL to match.
* **produces** (MediaType) - Response Content-type header.

**Example**

Register GET `/users` url.

```python
from py3server.web.mapping import GetMapping


@GetMapping('/users')
def get_users(self):
    pass
```

<br/>

### <span name="post-mapping">@PostMapping(_url_, _produces=MediaType.APPLICATION_JSON_)</span>

Decorate a function inside a class decorated with [@RestController](#rest-controller) to register the `url` with rules.

Only `HTTP POST` method will be matching.

The `url` can extract data if it contains `{<id>}` or with regex: `{<id>:<regex>}`.

To access extracted data of the `url` you need to use [PathParam](#path-param).

**Parameters**:

* **path** (str) - Request URL to match.
* **produces** (MediaType) - Response Content-type header.

**Example**

Register POST `/users` url.

```python
from py3server.web.mapping import PostMapping


@PostMapping('/users')
def create_user(self):
    pass
```

<br/>

### <span name="put-mapping">@PutMapping(_url_, _produces=MediaType.APPLICATION_JSON_)</span>

Decorate a function inside a class decorated with [@RestController](#rest-controller) to register the `url` with rules.

Only `HTTP PUT` method will be matching.

The `url` can extract data if it contains `{<id>}` or with regex: `{<id>:<regex>}`.

To access extracted data of the `url` you need to use [PathParam](#path-param).

**Parameters**:

* **path** (str) - Request URL to match.
* **produces** (MediaType) - Response Content-type header.

**Example**

Register PUT `/users` url.

```python
from py3server.web.mapping import PutMapping


@PutMapping('/users')
def update_user(self):
    pass
```

<br/>

### <span name="delete-mapping">@DeleteMapping(_url_, _produces=MediaType.APPLICATION_JSON_)</span>

Decorate a function inside a class decorated with [@RestController](#rest-controller) to register the `url` with rules.

Only `HTTP POST` method will be matching.

The `url` can extract data if it contains `{<id>}` or with regex: `{<id>:<regex>}`.

To access extracted data of the `url` you need to use [PathParam](#path-param).

**Parameters**:

* **path** (str) - Request URL to match.
* **produces** (MediaType) - Response Content-type header.

**Example**

Register DELETE `/users` url.

```python
from py3server.web.mapping import DeleteMapping


@DeleteMapping('/users')
def delete_users(self):
    pass
```

<br/>

## <span name="data">Data</span>

You can extract data of the request, and use it inside your function.

### <span name="path-param">@PathParam(_name_, __type_)</span>

Used for typing arguments of a function decorated with a [Mapping](#routing).

The function need to be inside a class decorated with [@RestController](#rest-controller) to be registered.

It will extract data of the URL if there is any used `id` matching `name`.

**Parameters**:

* **name** (str) - Should match existing id in route `url`.
* **_type** (type) - Expected variable type.

**Example**

Extract user id as `int`.

```python
from py3server.web.controllers import RestController
from py3server.web.mapping import GetMapping
from py3server.web.params import PathParam


@RestController('/users')
class MyController:

    @GetMapping('/{id}')
    def delete_users(self, user_id: PathParam('id', int)):
        pass
```

<br/>

### <span name="int-pp">@IntPP(_name_, __type_)</span>

Used for typing arguments of a function decorated with a [Mapping](#routing).

The function need to be inside a class decorated with [@RestController](#rest-controller) to be registered.

Work as [@PathParam](#path-param), but with a `int` type by default.

**Parameters**:

* **name** (str) - Should match existing id in route `url`.

**Example**

Extract `int` url variable.

```python
from py3server.web.controllers import RestController
from py3server.web.mapping import GetMapping
from py3server.web.params import IntPP


@RestController('/objects/add')
class MyController:

    @GetMapping('/{nb}')
    def delete_users(self, user_id: IntPP('nb')):
        pass
```

<br/>

### <span name="query-param">@QueryParam(_name_, __type_, default=None)</span>

Used for typing arguments of a function decorated with a [Mapping](#routing).

The function need to be inside a class decorated with [@RestController](#rest-controller) to be registered.

It will extract query params of the url for a matching `id`. It can have a default value.

**Parameters**:

* **name** (str) - Name of the query param.
* **_type** (type) - Type of the query param.
* **default** (any) - Default value if missing query param.

**Example**

Extract int `limit` and str `order` query params with `asc` as default value for `order`.

```python
from py3server.web.controllers import RestController
from py3server.web.mapping import GetMapping
from py3server.web.params import QueryParam


@RestController('/users')
class MyController:

    @GetMapping('/')
    def get_users(self, limit: QueryParam('limit', int), order: QueryParam('order', str, 'asc')):
        pass
```

<br/>

### <span name="int-qp">@IntQP(_name_, _default_=None)</span>

Used for typing arguments of a function decorated with a [Mapping](#routing).

The function need to be inside a class decorated with [@RestController](#rest-controller) to be registered.

Work as [@PathParam](#query-param), but with a `int` type by default.

**Parameters**:

* **name** (str) - Name of the query param.
* **default** (int) - Default value if missing query param.

**Example**

Extract `limit` query param with a default at 10.

```python
from py3server.web.controllers import RestController
from py3server.web.mapping import GetMapping
from py3server.web.params import IntQP


@RestController('/users')
class MyController:

    @GetMapping('/')
    def delete_users(self, limit: IntQP('limit', 10)):
        pass
```

<br/>

## <span name="response">Response</span>

All routes decorated with a [@Routing](#routing) decorator, should return a [@Response](#response) object.

### <span name="base-response">@Response(_name_, _default_=None)</span>

This object contains all the needed information for building the HTTP response send.

It needs to be returned by a function decorated with [@Routing](#routing).

**Parameters**:

* **status** (str) - Response status code.
* **content** (object) - Object returned serialized using response `Content-type`.

**Example**

Return a list of user with a `200` status code.

```python
from py3server.web.controllers import RestController
from py3server.web.mapping import GetMapping
from py3server.web import Response


@RestController('/users')
class MyController:

    @GetMapping('/')
    def get_users(self):
        users = get_all_users()
        return Response(200, users)
```

