"""
Copyright (c) ${YEAR} by Michal Perzel. All rights reserved.

License: MIT
"""

#: ------------------------------------------------ IMPORTS ------------------------------------------------
import sys
import pytest

from contextlib import contextmanager
from io import StringIO

#: Add the src directory to the Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# from wollwo_decorators.except_base_exception import ExceptBaseException
from wollwo_common import ExceptBaseException


#: ----------------------------------------------- VARIABLES -----------------------------------------------
def dummy_execution(text: str, *args, **kwargs):
    """Dummy method do be provided and tested if executed"""
    print(f"printing: {text}")


#: ------------------------------------------------- CLASS -------------------------------------------------
class BaseClass:
    test: bool = True

    def base_method(self, exc: int) -> int:
        """
        Method to raise exceptions to test ExceptException

        Attr:
            exc (int):
                What exception will method raise by providing specific integers
                    0 - No exception
                    1 - Exception()
                    2 - ValueError()
        """
        print(f'Name: {self.base_method.__qualname__}, Test: {self.test}')

        if exc not in range(1, 3):
            print(f'Dummy print {exc}')
            return exc

        elif exc == 1:
            print(f'Dummy print {exc}')
            raise BaseException(f'Dummy Exception {exc}')

        elif exc == 2:
            print(f'Dummy print {exc}')
            raise ValueError(f'Dummy ValueError {exc}')

    @ExceptBaseException(
        qualname='ExceptException.__init__',
        custom_logger=None,
        execute_on_exc=None,
        exit_on_exc=None,
        print_trace=True,
        silence_exc=False,
        pass_exc=False
    )
    def method_01_default_values(self, exc: int) -> int:
        """
        Method to raise exceptions to test ExceptException
        With default values in decoration
        """
        return self.base_method(exc)

    @ExceptBaseException(
        qualname='ExceptException.__init__',
        custom_logger=None,
        execute_on_exc=None,
        exit_on_exc=None,
        print_trace=False,
        silence_exc=True,
        pass_exc=False
    )
    def method_02_notrace_silence(self, exc: int) -> int:
        """
        Method to raise exceptions to test ExceptException
        default values changed for:
            - traceback will not be printed
            - excepted Exception will be silenced
        """
        return self.base_method(exc)

    @ExceptBaseException(
        qualname='ExceptException.__init__',
        custom_logger=None,
        execute_on_exc=None,
        exit_on_exc=10,
        print_trace=False,
        silence_exc=False,
        pass_exc=False
    )
    def method_03_notrace_exit(self, exc: int) -> int:
        """
        Method to raise exceptions to test ExceptException
        default values changed for:
            - traceback will not be printed
            - Before re-raising excepted Exception, sys.exit() will be called
            - exit code set to 10
        """
        return self.base_method(exc)

    @ExceptBaseException(
        qualname='ExceptException.__init__',
        custom_logger=None,
        execute_on_exc=dummy_execution,
        execute_on_exc_params=(['Dummy'],),
        exit_on_exc=None,
        print_trace=False,
        silence_exc=False,
        pass_exc=True
    )
    def method_04_execute_and_pass(self, exc: int) -> int:
        """
        Method to raise exceptions to test ExceptException
        default values changed for:
            - traceback will not be printed
            - excepted exception will be passed
            - before passing execution will be performed
        """
        return base_method(exc)


#: ------------------------------------------------ METHODS ------------------------------------------------
@contextmanager
def capture_output():
    """
    definition for capturing exit codes
    """
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield new_out, new_err
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def base_method(exc: int) -> int:
    """
    Method to raise exceptions to test ExceptException

    Attr:
        exc (int):
            What exception will method raise by providing specific integers
                0 - No exception
                1 - Exception()
                2 - ValueError()
    """

    if exc not in range(1, 3):
        print(f'Dummy print {exc}')
        return exc

    elif exc == 1:
        print(f'Dummy print {exc}')
        raise BaseException(f'Dummy Exception {exc}')

    elif exc == 2:
        print(f'Dummy print {exc}')
        raise ValueError(f'Dummy ValueError {exc}')


@ExceptBaseException(
    qualname='ExceptException.__init__',
    custom_logger=None,
    execute_on_exc=None,
    execute_on_exc_params=None,
    exit_on_exc=None,
    print_trace=True,
    silence_exc=False,
    pass_exc=False
)
def method_01_default_values(exc: int) -> int:
    """
    Method to raise exceptions to test ExceptException
    With default values in decoration
    """
    return base_method(exc)


@ExceptBaseException(
    qualname='ExceptException.__init__',
    custom_logger=None,
    execute_on_exc=None,
    execute_on_exc_params=None,
    exit_on_exc=None,
    print_trace=False,
    silence_exc=True,
    pass_exc=False
)
def method_02_notrace_silence(exc: int) -> int:
    """
    Method to raise exceptions to test ExceptException
    default values changed for:
        - traceback will not be printed
        - excepted Exception will be silenced
    """
    return base_method(exc)


@ExceptBaseException(
    qualname='ExceptException.__init__',
    custom_logger=None,
    execute_on_exc=None,
    execute_on_exc_params=None,
    exit_on_exc=10,
    print_trace=False,
    silence_exc=False,
    pass_exc=False
)
def method_03_notrace_exit(exc: int) -> int:
    """
    Method to raise exceptions to test ExceptException
    default values changed for:
        - traceback will not be printed
        - Before re-raising excepted Exception, sys.exit() will be called
        - exit code set to 10
    """
    return base_method(exc)

@ExceptBaseException(
    qualname='ExceptException.__init__',
    custom_logger=None,
    execute_on_exc=dummy_execution,
    execute_on_exc_params=(['Dummy'], {}),
    exit_on_exc=None,
    print_trace=False,
    silence_exc=False,
    pass_exc=True
)
def method_04_execute_and_pass(exc: int) -> int:
    """
    Method to raise exceptions to test ExceptException
    default values changed for:
        - traceback will not be printed
        - excepted exception will be passed
        - before passing execution will be performed
    """
    return base_method(exc)


# Define the fixture
@pytest.fixture(params=[0, 1, 2])
def exc_value(request):
    return request.param


def test_exceptexception_class_as_method_decorator_01(exc_value, capsys):
    """
    testing ExceptException

    method_01_default_values
    """

    #: #################################
    #: No Exception
    #: #################################

    if exc_value == 0:
        result1 = method_01_default_values(exc_value)
        test_class = BaseClass()
        result2 = test_class.method_01_default_values(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert result1 == 0
        assert result2 == 0
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Dummy print 0'
        assert captured.out.splitlines()[1] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[2] == f'Dummy print 0'

    #: #################################
    #: Exception
    #: #################################

    elif exc_value == 1:
        with pytest.raises(BaseException) as exc_info:
            method_01_default_values(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy Exception 1"
        assert len(captured.out.splitlines()) == 5
        assert captured.out.splitlines()[0] == f'Dummy print 1'
        assert captured.out.splitlines()[1] == f'ERROR: method_01_default_values : BaseException: Dummy Exception 1'
        assert (captured.out.splitlines()[2] ==
                f'DEBUG: method_01_default_values : BaseException: Printing trace of "BaseException"')
        assert (captured.out.splitlines()[3] ==
                f'============================== Traceback START ==============================')
        assert (captured.out.splitlines()[4] ==
                f'=============================== Traceback END ===============================')

        with pytest.raises(BaseException) as exc_info:
            test_class = BaseClass()
            test_class.method_01_default_values(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy Exception 1"
        assert len(captured.out.splitlines()) == 6
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 1'
        assert (captured.out.splitlines()[2] ==
                f'ERROR: BaseClass.method_01_default_values : BaseException: Dummy Exception 1')
        assert (captured.out.splitlines()[3] ==
                'DEBUG: BaseClass.method_01_default_values : BaseException: Printing trace of "BaseException"')
        assert (captured.out.splitlines()[4] ==
                f'============================== Traceback START ==============================')
        assert (captured.out.splitlines()[5] ==
                f'=============================== Traceback END ===============================')

    #: #################################
    #: ValueError
    #: #################################

    elif exc_value == 2:
        with pytest.raises(ValueError) as exc_info:
            method_01_default_values(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 2
        assert captured.out.splitlines()[0] == f'Dummy print 2'
        assert (captured.out.splitlines()[1] ==
                f'DEBUG: method_01_default_values : Passing on raised exception: "ValueError: Dummy ValueError 2"')

        with pytest.raises(ValueError) as exc_info:
            test_class = BaseClass()
            test_class.method_01_default_values(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 2'
        assert (captured.out.splitlines()[2] ==
                f'DEBUG: BaseClass.method_01_default_values : Passing on raised exception: '
                f'"ValueError: Dummy ValueError 2"')


def test_exceptexception_class_as_method_decorator_02(exc_value, capsys):
    """
    testing ExceptException

    method_02_notrace_silence
    """

    #: #################################
    #: No Exception
    #: #################################

    if exc_value == 0:
        result1 = method_02_notrace_silence(exc_value)
        test_class = BaseClass()
        result2 = test_class.method_02_notrace_silence(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert result1 == 0
        assert result2 == 0
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Dummy print 0'
        assert captured.out.splitlines()[1] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[2] == f'Dummy print 0'

    #: #################################
    #: Exception
    #: #################################

    elif exc_value == 1:
        result3 = method_02_notrace_silence(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert result3 is None
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Dummy print 1'
        assert captured.out.splitlines()[1] == f'ERROR: method_02_notrace_silence : BaseException: Dummy Exception 1'


        test_class = BaseClass()
        result4 = test_class.method_02_notrace_silence(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert result4 is None
        assert len(captured.out.splitlines()) == 4
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 1'
        assert (captured.out.splitlines()[2] ==
                f'ERROR: BaseClass.method_02_notrace_silence : BaseException: Dummy Exception 1')

    #: #################################
    #: ValueError
    #: #################################

    elif exc_value == 2:
        with pytest.raises(ValueError) as exc_info:
            method_02_notrace_silence(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 2
        assert captured.out.splitlines()[0] == f'Dummy print 2'
        assert (captured.out.splitlines()[1] ==
                f'DEBUG: method_02_notrace_silence : Passing on raised exception: "ValueError: Dummy ValueError 2"')

        with pytest.raises(ValueError) as exc_info:
            test_class = BaseClass()
            test_class.method_02_notrace_silence(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 2'
        assert (captured.out.splitlines()[2] ==
                f'DEBUG: BaseClass.method_02_notrace_silence : Passing on raised exception: '
                f'"ValueError: Dummy ValueError 2"')


def test_exceptexception_class_as_method_decorator_03(exc_value, capsys):
    """
    testing ExceptException

    method_03_notrace_exit
    """

    #: #################################
    #: No Exception
    #: #################################

    if exc_value == 0:
        result1 = method_03_notrace_exit(exc_value)
        test_class = BaseClass()
        result2 = test_class.method_03_notrace_exit(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert result1 == 0
        assert result2 == 0
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Dummy print 0'
        assert captured.out.splitlines()[1] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[2] == f'Dummy print 0'

    #: #################################
    #: Exception
    #: #################################

    elif exc_value == 1:
        #: test if Exit code is correct
        with pytest.raises(SystemExit) as excinfo:
            with capture_output():
                result3 = method_03_notrace_exit(exc_value)

        #: Assert
        assert excinfo.value.code == 10

        #: test all outputs are correct
        with pytest.raises(SystemExit) as excinfo:
            method_03_notrace_exit(exc_value)

        # Capture the output
        captured = capsys.readouterr()

        # Assert
        assert excinfo.type is SystemExit
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Dummy print 1'
        assert (captured.out.splitlines()[1] ==
                f'ERROR: method_03_notrace_exit : BaseException: Dummy Exception 1')
        assert captured.out.splitlines()[2] == f'ERROR: method_03_notrace_exit : BaseException: Exiting with 10'

        #: test if Exit code is correct
        with pytest.raises(SystemExit) as excinfo:
            with capture_output():
                test_class = BaseClass()
                test_class.method_03_notrace_exit(exc_value)

        #: Assert
        assert excinfo.value.code == 10

        #: test all outputs are correct
        with pytest.raises(SystemExit) as excinfo:
            test_class = BaseClass()
            test_class.method_03_notrace_exit(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert excinfo.type is SystemExit
        assert len(captured.out.splitlines()) == 4
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 1'
        assert (captured.out.splitlines()[2] ==
                f'ERROR: BaseClass.method_03_notrace_exit : BaseException: Dummy Exception 1')
        assert (captured.out.splitlines()[3] ==
                f'ERROR: BaseClass.method_03_notrace_exit : BaseException: Exiting with 10')

    #: #################################
    #: ValueError
    #: #################################

    elif exc_value == 2:
        with pytest.raises(ValueError) as exc_info:
            method_03_notrace_exit(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 2
        assert captured.out.splitlines()[0] == f'Dummy print 2'
        assert (captured.out.splitlines()[1] ==
                f'DEBUG: method_03_notrace_exit : Passing on raised exception: "ValueError: Dummy ValueError 2"')

        with pytest.raises(ValueError) as exc_info:
            test_class = BaseClass()
            test_class.method_03_notrace_exit(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 2'
        assert (captured.out.splitlines()[2] ==
                f'DEBUG: BaseClass.method_03_notrace_exit : Passing on raised exception: '
                f'"ValueError: Dummy ValueError 2"')


def test_exceptexception_class_as_method_decorator_04(exc_value, capsys):
    """
    testing ExceptException

    method_04_execute_and_pass
    """

    #: #################################
    #: No Exception
    #: #################################

    if exc_value == 0:
        result1 = method_04_execute_and_pass(exc_value)
        test_class = BaseClass()
        result2 = test_class.method_04_execute_and_pass(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert result1 == 0
        assert result2 == 0
        assert len(captured.out.splitlines()) == 2
        assert captured.out.splitlines()[0] == f'Dummy print 0'
        assert captured.out.splitlines()[1] == f'Dummy print 0'

    #: #################################
    #: Exception
    #: #################################

    elif exc_value == 1:
        #: test custom method execution and passing Exception
        with pytest.raises(BaseException, match='Dummy Exception 1'):
            result3 = method_04_execute_and_pass(exc_value)

        #: Capture the output
        captured = capsys.readouterr()
        assert len(captured.out.splitlines()) == 5
        assert captured.out.splitlines()[0] == f'Dummy print 1'
        assert (captured.out.splitlines()[1] ==
                f'ERROR: method_04_execute_and_pass : BaseException: Dummy Exception 1')
        assert (captured.out.splitlines()[2] ==
                f'DEBUG: method_04_execute_and_pass : BaseException: Executing custom method')
        assert (captured.out.splitlines()[3] ==
                f'printing: Dummy')
        assert (captured.out.splitlines()[4] ==
                f'DEBUG: method_04_execute_and_pass : Passing on raised exception: "BaseException: Dummy Exception 1"')

    #: #################################
    #: ValueError
    #: #################################

    elif exc_value == 2:
        with pytest.raises(ValueError) as exc_info:
            method_04_execute_and_pass(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 2
        assert captured.out.splitlines()[0] == f'Dummy print 2'
        assert (captured.out.splitlines()[1] ==
                f'DEBUG: method_04_execute_and_pass : Passing on raised exception: "ValueError: Dummy ValueError 2"')

        with pytest.raises(ValueError) as exc_info:
            test_class = BaseClass()
            test_class.method_04_execute_and_pass(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 2
        assert captured.out.splitlines()[0] == f'Dummy print 2'
        assert (captured.out.splitlines()[1] ==
                f'DEBUG: BaseClass.method_04_execute_and_pass : Passing on raised exception: '
                f'"ValueError: Dummy ValueError 2"')


def test_exceptexception_class_as_contextmanager_01(exc_value, capsys):
    """
    testing ExceptException

    base_method in context manager with default values
    """

    #: #################################
    #: No Exception
    #: #################################

    if exc_value == 0:
        with ExceptBaseException(
                qualname='WithContextManager.test',
                custom_logger=None,
                execute_on_exc=None,
                exit_on_exc=None,
                print_trace=True,
                silence_exc=False,
                pass_exc=False
        ) as test1:
            result1 = base_method(exc_value)
            test_class = BaseClass()
            result2 = test_class.base_method(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert result1 == 0
        assert result2 == 0
        assert len(captured.out.splitlines()) == 3
        assert not test1.exception_responses
        assert captured.out.splitlines()[0] == f'Dummy print 0'
        assert captured.out.splitlines()[1] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[2] == f'Dummy print 0'

    #: #################################
    #: Exception
    #: #################################

    elif exc_value == 1:
        with pytest.raises(BaseException) as exc_info:
            with ExceptBaseException(
                    qualname='WithContextManager.test',
                    custom_logger=None,
                    execute_on_exc=None,
                    exit_on_exc=None,
                    print_trace=True,
                    silence_exc=False,
                    pass_exc=False
            ) as test2:
                base_method(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy Exception 1"
        assert len(captured.out.splitlines()) == 5
        assert len(test2.exception_responses) == 1
        assert test2.exception_responses[0] == {
            'exception': 'BaseException',
            'response': 'BaseException: Dummy Exception 1'
        }
        assert captured.out.splitlines()[0] == f'Dummy print 1'
        assert captured.out.splitlines()[1] == f'ERROR: WithContextManager.test : BaseException: Dummy Exception 1'
        assert (captured.out.splitlines()[2] ==
                'DEBUG: WithContextManager.test : BaseException: Printing trace of "BaseException"')
        assert (captured.out.splitlines()[3] ==
                f'============================== Traceback START ==============================')
        assert (captured.out.splitlines()[4] ==
                f'=============================== Traceback END ===============================')

        with pytest.raises(BaseException) as exc_info:
            with ExceptBaseException(
                    qualname='WithContextManager.test',
                    custom_logger=None,
                    execute_on_exc=None,
                    exit_on_exc=None,
                    print_trace=True,
                    silence_exc=False,
                    pass_exc=False
            ) as test3:
                test_class = BaseClass()
                test_class.base_method(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy Exception 1"
        assert len(captured.out.splitlines()) == 6
        assert len(test3.exception_responses) == 1
        assert test3.exception_responses[0] == {
            'exception': 'BaseException',
            'response': 'BaseException: Dummy Exception 1'
        }
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 1'
        assert captured.out.splitlines()[2] == f'ERROR: WithContextManager.test : BaseException: Dummy Exception 1'
        assert (captured.out.splitlines()[3] ==
                'DEBUG: WithContextManager.test : BaseException: Printing trace of "BaseException"')
        assert (captured.out.splitlines()[4] ==
                f'============================== Traceback START ==============================')
        assert (captured.out.splitlines()[5] ==
                f'=============================== Traceback END ===============================')

    #: #################################
    #: ValueError
    #: #################################

    elif exc_value == 2:
        with pytest.raises(ValueError) as exc_info:
            with ExceptBaseException(
                    qualname='WithContextManager.test',
                    custom_logger=None,
                    execute_on_exc=None,
                    exit_on_exc=None,
                    print_trace=True,
                    silence_exc=False,
                    pass_exc=False
            ) as test4:
                base_method(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 2
        assert not test4.exception_responses
        assert captured.out.splitlines()[0] == f'Dummy print 2'
        assert (captured.out.splitlines()[1] ==
                f'DEBUG: WithContextManager.test : Passing on raised exception: "ValueError: Dummy ValueError 2"')

        with pytest.raises(ValueError) as exc_info:
            with ExceptBaseException(
                    qualname='WithContextManager.test',
                    custom_logger=None,
                    execute_on_exc=None,
                    exit_on_exc=None,
                    print_trace=True,
                    silence_exc=False,
                    pass_exc=False
            ):
                test_class = BaseClass()
                test_class.base_method(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 2'
        assert (captured.out.splitlines()[2] ==
                f'DEBUG: WithContextManager.test : Passing on raised exception: "ValueError: Dummy ValueError 2"')


def test_exceptexception_class_as_contextmanager_02(exc_value, capsys):
    """
    testing ExceptException

    base_method in context manager with no trace and silence excepted exception
    """

    #: #################################
    #: No Exception
    #: #################################

    if exc_value == 0:
        with ExceptBaseException(
                qualname='WithContextManager.test',
                custom_logger=None,
                execute_on_exc=None,
                exit_on_exc=None,
                print_trace=False,
                silence_exc=True,
                pass_exc=False
        ):
            result1 = base_method(exc_value)
            test_class = BaseClass()
            result2 = test_class.base_method(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert result1 == 0
        assert result2 == 0
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Dummy print 0'
        assert captured.out.splitlines()[1] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[2] == f'Dummy print 0'

    #: #################################
    #: Exception
    #: #################################

    elif exc_value == 1:
        with ExceptBaseException(
                qualname='WithContextManager.test',
                custom_logger=None,
                execute_on_exc=None,
                exit_on_exc=None,
                print_trace=False,
                silence_exc=True,
                pass_exc=False
        ):
            result3 = base_method(exc_value)
            assert result3 is None

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Dummy print 1'
        assert captured.out.splitlines()[1] == f'ERROR: WithContextManager.test : BaseException: Dummy Exception 1'

        with ExceptBaseException(
                qualname='WithContextManager.test',
                custom_logger=None,
                execute_on_exc=None,
                exit_on_exc=None,
                print_trace=False,
                silence_exc=True,
                pass_exc=False
        ):
            test_class = BaseClass()
            result4 = test_class.base_method(exc_value)
            assert result4 is None

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert len(captured.out.splitlines()) == 4
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 1'
        assert (captured.out.splitlines()[2] ==
                f'ERROR: WithContextManager.test : BaseException: Dummy Exception 1')

    #: #################################
    #: ValueError
    #: #################################

    elif exc_value == 2:
        with pytest.raises(ValueError) as exc_info:
            with ExceptBaseException(
                    qualname='WithContextManager.test',
                    custom_logger=None,
                    execute_on_exc=None,
                    exit_on_exc=None,
                    print_trace=False,
                    silence_exc=True,
                    pass_exc=False
            ):
                base_method(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 2
        assert captured.out.splitlines()[0] == f'Dummy print 2'
        assert (captured.out.splitlines()[1] ==
                f'DEBUG: WithContextManager.test : Passing on raised exception: "ValueError: Dummy ValueError 2"')

        with pytest.raises(ValueError) as exc_info:
            with ExceptBaseException(
                    qualname='WithContextManager.test',
                    custom_logger=None,
                    execute_on_exc=None,
                    exit_on_exc=None,
                    print_trace=False,
                    silence_exc=True,
                    pass_exc=False
            ):
                test_class = BaseClass()
                test_class.base_method(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 2'
        assert (captured.out.splitlines()[2] ==
                f'DEBUG: WithContextManager.test : Passing on raised exception: "ValueError: Dummy ValueError 2"')


def test_exceptexception_class_as_contextmanager_03(exc_value, capsys):
    """
    testing ExceptException

    base_method in context manager with no trace and exit on exception
    """

    #: #################################
    #: No Exception
    #: #################################

    if exc_value == 0:
        with ExceptBaseException(
                qualname='WithContextManager.test',
                custom_logger=None,
                execute_on_exc=None,
                exit_on_exc=None,
                print_trace=False,
                silence_exc=False,
                pass_exc=False
        ):
            result1 = base_method(exc_value)
            test_class = BaseClass()
            result2 = test_class.base_method(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert result1 == 0
        assert result2 == 0
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Dummy print 0'
        assert captured.out.splitlines()[1] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[2] == f'Dummy print 0'

    #: #################################
    #: Exception
    #: #################################

    elif exc_value == 1:
        #: test if Exit code is correct
        with pytest.raises(SystemExit) as excinfo:
            with capture_output():
                with ExceptBaseException(
                        qualname='WithContextManager.test',
                        custom_logger=None,
                        execute_on_exc=None,
                        exit_on_exc=10,
                        print_trace=False,
                        silence_exc=False,
                        pass_exc=False
                ):
                    base_method(exc_value)

        #: Assert
        assert excinfo.value.code == 10

        #: test all outputs are correct
        with pytest.raises(SystemExit) as excinfo:
            with ExceptBaseException(
                    qualname='WithContextManager.test',
                    custom_logger=None,
                    execute_on_exc=None,
                    exit_on_exc=10,
                    print_trace=False,
                    silence_exc=False,
                    pass_exc=False
            ):
                base_method(exc_value)

        # Capture the output
        captured = capsys.readouterr()

        # Assert
        assert excinfo.type is SystemExit
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Dummy print 1'
        assert (captured.out.splitlines()[1] ==
                f'ERROR: WithContextManager.test : BaseException: Dummy Exception 1')
        assert captured.out.splitlines()[2] == f'ERROR: WithContextManager.test : BaseException: Exiting with 10'

        #: test if Exit code is correct
        with pytest.raises(SystemExit) as excinfo:
            with capture_output():
                with ExceptBaseException(
                        qualname='WithContextManager.test',
                        custom_logger=None,
                        execute_on_exc=None,
                        exit_on_exc=10,
                        print_trace=False,
                        silence_exc=False,
                        pass_exc=False
                ):
                    test_class = BaseClass()
                    test_class.base_method(exc_value)

        #: Assert
        assert excinfo.value.code == 10

        #: test all outputs are correct
        with pytest.raises(SystemExit) as excinfo:
            with ExceptBaseException(
                    qualname='WithContextManager.test',
                    custom_logger=None,
                    execute_on_exc=None,
                    exit_on_exc=10,
                    print_trace=False,
                    silence_exc=False,
                    pass_exc=False
            ):
                test_class = BaseClass()
                test_class.base_method(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert excinfo.type is SystemExit
        assert len(captured.out.splitlines()) == 4
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 1'
        assert (captured.out.splitlines()[2] ==
                f'ERROR: WithContextManager.test : BaseException: Dummy Exception 1')
        assert captured.out.splitlines()[
                   3] == f'ERROR: WithContextManager.test : BaseException: Exiting with 10'

    #: #################################
    #: ValueError
    #: #################################

    elif exc_value == 2:
        with pytest.raises(ValueError) as exc_info:
            with ExceptBaseException(
                    qualname='WithContextManager.test',
                    custom_logger=None,
                    execute_on_exc=None,
                    exit_on_exc=10,
                    print_trace=False,
                    silence_exc=False,
                    pass_exc=False
            ):
                base_method(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 2
        assert captured.out.splitlines()[0] == f'Dummy print 2'
        assert (captured.out.splitlines()[1] ==
                f'DEBUG: WithContextManager.test : Passing on raised exception: "ValueError: Dummy ValueError 2"')

        with pytest.raises(ValueError) as exc_info:
            with ExceptBaseException(
                    qualname='WithContextManager.test',
                    custom_logger=None,
                    execute_on_exc=None,
                    exit_on_exc=10,
                    print_trace=False,
                    silence_exc=False,
                    pass_exc=False
            ):
                test_class = BaseClass()
                test_class.base_method(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy ValueError 2"
        assert len(captured.out.splitlines()) == 3
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 2'
        assert (captured.out.splitlines()[2] ==
                f'DEBUG: WithContextManager.test : Passing on raised exception: "ValueError: Dummy ValueError 2"')

#: [ ] ToDo: Add wollwo_decorators for execute and pass excepted Exception


#: ------------------------------------------------- BODY --------------------------------------------------
if __name__ == '__main__':
    pass
