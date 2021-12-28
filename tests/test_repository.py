from py3server.app.repository import Repository
from py3server.constants import Decorator
from py3server.context import Context


def test_repository_init():
    # GIVEN
    context: Context = Context()

    # WHEN
    repository: Repository = Repository()

    # THEN
    assert repository.context == context
    print(context.decorators)
    assert context.decorators[Decorator.REPOSITORY][0] == repository


def test_repository_call():
    # GIVEN
    context: Context = Context()
    repository: Repository = Repository()

    class FakeClass:
        pass

    # WHEN
    repository(FakeClass)

    # THEN
    assert isinstance(repository.clazz, FakeClass)
    assert context.instances[hash(FakeClass)] == repository.clazz
