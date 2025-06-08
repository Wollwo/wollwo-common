"""
Copyright (c) 2025 perzelmichal@gmail.com
All rights reserved.
"""
#: ------------------------------------------------ IMPORTS ------------------------------------------------
import sys
import traceback

from dataclasses import dataclass, field, fields
from functools import wraps
from logging import Logger
from typing import Optional, Any

__all__ = [
    'ExceptBaseException'
]
#: ----------------------------------------------- VARIABLES -----------------------------------------------


#: ------------------------------------------------- CLASS -------------------------------------------------
@dataclass
class ExceptBaseException:
    """
    Context manager / Decorator for excepting BaseException.
    It will pass through any other type of exception

    Handles "BaseException" Exception:
      - exit on exception
      - silence exception
      - print traceback on exception

    Parameters:
        qualname (str):
        custom_logger (Logger): Default None
            logger which should be used to log/print messages
        execute_on_exc (bool): Default False
            if True, it will execute self.execution_list()
            executed after logger and before trace
        exit_code (int): Default 1
            provide exit code, from 0-255
        exit_on_exc (bool): Default False
            exit on exception, return provided exit code
            if True, silence_exc will not be executed
        print_trace (bool): Default True
            will print traceback before raisin/exiting/silencing exception
            print trace just before exit or silence
        silence_exc (bool): Default False
            silence exception, if not exited first

    Exceptions:
        TypeError: raised by:
            - __setattr__() on provided wrong attribute Type
    """

    qualname: str = field(default_factory=lambda: ExceptBaseException.__init__.__qualname__)
    custom_logger: Optional[Logger] = None
    execute_on_exc: bool = field(default=False)
    exit_code: int = field(default=1)
    exit_on_exc: bool = field(default=False)
    print_trace: bool = field(default=True)
    silence_exc: bool = field(default=False)

    #: internal attributes not meant to be changed
    _expected_exception: BaseException = field(default=BaseException, init=False, repr=False)
    __rep: int = field(default=30, init=False, repr=False)

    def __enter__(self):
        """Enter context manager"""
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Exception handling and other cleaning tasks"""

        #: Check for excepted exception
        if exc_type is not None:
            if (isinstance(exc_type(), BaseException) and
                    exc_type.__name__ == self._expected_exception.__name__
            ):
                #: logger
                self.__internal_logger('error', f'{exc_type.__name__}: {exc_value}')

                if self.execute_on_exc:
                    self.execution_list()

                #: Traceback
                if self.print_trace:
                    self.__print_traceback(exc_type, exc_value, exc_tb)

                #: Exit
                if self.exit_on_exc:
                    self.__internal_logger('error', f'{exc_type.__name__}: Exiting with {self.exit_code}')
                    sys.exit(self.exit_code)

                #: ToDo: 01 - check possibility to return some value if there is exception
                #: ToDo:    some code injection ?
                #: ToDo:    what should be done if there is exception
                #: ToDo:    setattr(CM, 'd') -> with CM.something
                #: ToDo:    decorator will have in post_init setattr() tied to attribute

                #: silence
                return self.silence_exc if isinstance(self.silence_exc, bool) else False


            self.__internal_logger('debug', f'Passing on raised exception: "{exc_type.__name__}:{exc_value}"')
        pass

    def __call__(self, func):
        """Decorator"""

        self.qualname = func.__qualname__

        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper

    def __setattr__(self, name, value):
        """
        setting and checking attributes based on expected annotations

        Be aware that you must specify exact types, "typing" types can be used
        """

        attributes = {attr.name: attr.type for attr in fields(self)}

        #: Check provided types for all attributes, raise TypeError if there is no match
        if name in attributes.keys() and not isinstance(value, attributes[name]):
            raise TypeError(f'Expected "{name}" to be of type "{attributes[name]}", got {type(value).__name__}')

        # #: If some attributes must have specific values
        # if name == "example":
        #     value = value.lower()
        #     if value not in ['A', 'B']:
        #         raise ValueError(f"Expected '{name}' to be in {['A', 'B']}")

        if hasattr(super(), '__setattr__'):
            super().__setattr__(name, value)

    def __internal_logger(self, level: Optional[str], text: Optional[str], /) -> None:
        """
        internal logging mechanism for class

        Parameters:
            level (str):
                one of ['debug', 'info', 'warning', 'error', 'critical']
            text (str):
                printed
        """

        if self.custom_logger is None:
            expected_values = ['debug', 'info', 'warning', 'error', 'critical']
            level = level.upper() if level.lower() in expected_values else 'INFO'

            text = str(text)

            print(f'{level}: {self.qualname} : {text}')

        return

    def __print_traceback(self, exc_type, exc_value, traceback_obj):
        """
        print captured traceback
        """
        print(f'{"=" * self.__rep} Traceback START {"=" * self.__rep}')
        traceback.print_exception(exc_type, exc_value, traceback_obj)
        print(f'{"=" * (self.__rep + 1)} Traceback END {"=" * (self.__rep + 1)}')

    def execution_list(self) -> Any:
        raise NotImplemented()

#: ------------------------------------------------ METHODS ------------------------------------------------


#: ------------------------------------------------- BODY --------------------------------------------------
if __name__ == '__main__':
    pass
