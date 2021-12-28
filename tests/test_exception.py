from pytest_mock import MockerFixture

from py3server.app.exception import ExceptionHandler
from py3server.context import Context


def test_exception_handler_init():
    # GIVEN
    context: Context = Context()

    # WHEN
    exception_handler: ExceptionHandler = ExceptionHandler()

    # THEN
    assert exception_handler.context == context
    assert exception_handler.types == [Exception]
    assert context.exception_handlers[0] == exception_handler


def test_exception_handler_init_with_types():
    # GIVEN
    context: Context = Context()

    class FakeExceptionA:
        pass

    class FakeExceptionB:
        pass

    # WHEN
    exception_handler: ExceptionHandler = ExceptionHandler(types=[FakeExceptionA, FakeExceptionB])

    # THEN
    assert exception_handler.context == context
    assert exception_handler.types == [FakeExceptionA, FakeExceptionB]
    assert context.exception_handlers[0] == exception_handler


def test_exception_handler_call():
    # GIVEN
    exception_handler: ExceptionHandler = ExceptionHandler()

    class FakeException:
        pass

    # WHEN
    fake_exception: FakeException = exception_handler(FakeException)

    # THEN
    assert isinstance(fake_exception, FakeException)
    assert exception_handler.clazz == fake_exception


def test_exception_handler_accept_when_true():
    # GIVEN
    class FakeExceptionA:
        pass

    exception_handler: ExceptionHandler = ExceptionHandler(types=[FakeExceptionA])

    # WHEN
    accept: bool = exception_handler.accept(FakeExceptionA())

    # THEN
    assert accept


def test_exception_handler_accept_when_false():
    # GIVEN
    class FakeExceptionA:
        pass

    exception_handler: ExceptionHandler = ExceptionHandler()

    # WHEN
    accept: bool = exception_handler.accept(FakeExceptionA())

    # THEN
    assert not accept


def test_exception_handler_handle_exception(mocker: MockerFixture):
    # GIVEN
    exception_handler: ExceptionHandler = ExceptionHandler()
    raised_exception: Exception = Exception()

    class FakeException:
        def handle_exception(self, exception):
            pass

    handle_exception_spy: mocker.MagicMock = mocker.spy(FakeException, 'handle_exception')

    exception_handler(FakeException)

    # WHEN
    exception_handler.handle_exception(raised_exception)

    # THEN
    handle_exception_spy.assert_called_once_with(exception_handler.clazz, raised_exception)
