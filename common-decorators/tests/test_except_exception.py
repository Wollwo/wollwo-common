"""
Copyright (c) 2025 perzelmichal@gmail.com
All rights reserved.
"""
#: ------------------------------------------------ IMPORTS ------------------------------------------------
import os
import sys
import pytest
import re

from contextlib import contextmanager
from io import StringIO
from typing import Optional
from logging import Logger

#: Add the src directory to the Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from common_decorators.except_exception import ExceptBaseException


#: ----------------------------------------------- VARIABLES -----------------------------------------------


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
        exit_code=1,
        exit_on_exc=False,
        print_trace=True,
        silence_exc=False
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
        exit_code=1,
        exit_on_exc=False,
        print_trace=False,
        silence_exc=True
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
        exit_code=10,
        exit_on_exc=True,
        print_trace=False,
        silence_exc=False
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
    exit_code=1,
    exit_on_exc=False,
    print_trace=True,
    silence_exc=False
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
    exit_code=1,
    exit_on_exc=False,
    print_trace=False,
    silence_exc=True
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
    exit_code=10,
    exit_on_exc=True,
    print_trace=False,
    silence_exc=False
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
        assert len(captured.out.splitlines()) == 4
        assert captured.out.splitlines()[0] == f'Dummy print 1'
        assert captured.out.splitlines()[1] == f'ERROR: method_01_default_values : BaseException: Dummy Exception 1'
        assert (captured.out.splitlines()[2] ==
                f'============================== Traceback START ==============================')
        assert (captured.out.splitlines()[3] ==
                f'=============================== Traceback END ===============================')

        with pytest.raises(BaseException) as exc_info:
            test_class = BaseClass()
            test_class.method_01_default_values(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert str(exc_info.value) == "Dummy Exception 1"
        assert len(captured.out.splitlines()) == 5
        assert captured.out.splitlines()[0] == f'Name: BaseClass.base_method, Test: True'
        assert captured.out.splitlines()[1] == f'Dummy print 1'
        assert captured.out.splitlines()[2] == f'ERROR: BaseClass.method_01_default_values : BaseException: Dummy Exception 1'
        assert (captured.out.splitlines()[3] ==
                f'============================== Traceback START ==============================')
        assert (captured.out.splitlines()[4] ==
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
                f'DEBUG: method_01_default_values : Passing on raised exception: "ValueError:Dummy ValueError 2"')

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
                f'DEBUG: BaseClass.method_01_default_values : Passing on raised exception: "ValueError:Dummy ValueError 2"')


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
        assert len(captured.out.splitlines()) == 2
        assert captured.out.splitlines()[0] == f'Dummy print 1'
        assert captured.out.splitlines()[1] == f'ERROR: method_02_notrace_silence : BaseException: Dummy Exception 1'


        test_class = BaseClass()
        result4 = test_class.method_02_notrace_silence(exc_value)

        #: capture print() output
        captured = capsys.readouterr()

        #: Assert
        assert result4 is None
        assert len(captured.out.splitlines()) == 3
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
                f'DEBUG: method_02_notrace_silence : Passing on raised exception: "ValueError:Dummy ValueError 2"')

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
                f'DEBUG: BaseClass.method_02_notrace_silence : Passing on raised exception: "ValueError:Dummy ValueError 2"')


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
        assert captured.out.splitlines()[3] == f'ERROR: BaseClass.method_03_notrace_exit : BaseException: Exiting with 10'

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
                f'DEBUG: method_03_notrace_exit : Passing on raised exception: "ValueError:Dummy ValueError 2"')

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
                f'DEBUG: BaseClass.method_03_notrace_exit : Passing on raised exception: "ValueError:Dummy ValueError 2"')


def test_exceptexception_class_as_contextmanager_01(exc_value, capsys):
    """
    testing ExceptException

    method_01_default_values
    """
    pass


def test_exceptexception_class_as_contextmanager_02(exc_value, capsys):
    """
    testing ExceptException

    method_02_notrace_silence
    """
    pass


def test_exceptexception_class_as_contextmanager_03(exc_value, capsys):
    """
    testing ExceptException

    method_03_notrace_exit
    """
    pass


#: ------------------------------------------------- BODY --------------------------------------------------
if __name__ == '__main__':
    pass
