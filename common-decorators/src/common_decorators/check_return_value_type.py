"""
Copyright (c) 2025 perzelmichal@gmail.com
All rights reserved.
"""
#: ------------------------------------------------ IMPORTS ------------------------------------------------
from functools import wraps
from inspect import isfunction
from typing import Any, Tuple, Type

__all__ = [
    'CheckReturnValueType'
]

#: ----------------------------------------------- VARIABLES -----------------------------------------------


#: ------------------------------------------------- CLASS -------------------------------------------------
class CheckReturnValueType:
    """
    Functions as decorator and context manager for checking if
    return value of wrapped function return value of expected type

    raises:
        TypeError

    """
    def __init__(
            self,
            expected_type: Type[Any],
            /, *,
            use_annotation: bool = False
            # raise_exception: bool = True
    ):
        """

        Attr:
            expected_type (Type[Any]):
                what type must be returned value of wrapped method
            use_annotation (bool):
                use annotation as expected_type,
                defaults to expected_type if annotation is not provided
            # raise_exception (bool):
            #     if True, raise TypeError exception if returned value is of wrong type

        """
        self.expected_type = expected_type
        self.use_annotation = use_annotation
        # self.raise_exception = raise_exception

    def __enter__(self):
        """You can perform setup actions here if needed"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """You can perform cleanup actions here if needed"""
        pass

    def check(self, func, *args, **kwargs):
        """
        run wrapped function, check if return value of correct type
        raise TypeError exception if not (raise_exception=True)

        returns:
            func
        """
        if not isfunction(func):
            raise TypeError(f'Expected "func" to be callable function, got {type(func).__name__}')

        #: check if __annotation__ are provided and self.use_annotation=True
        expected_func_type = self.expected_type
        if self.use_annotation:
            expected_func_type = func.__annotations__.get('return', self.expected_type)

        #: run wrapped function
        result = func(*args, **kwargs)

        #: check return value
        if not isinstance(result, expected_func_type):
            # if self.raise_exception:
            #     raise TypeError(f"Expected return type {self.expected_type}, got {type(result)}")
            raise TypeError(f"Expected return type {expected_func_type}, got {type(result)}")

        return result

    def __call__(self, func):
        """can be used as decorator"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return self.check(func, *args, **kwargs)
        return wrapper



#: ------------------------------------------------ METHODS ------------------------------------------------


#: ------------------------------------------------- BODY --------------------------------------------------
if __name__ == '__main__':
    pass
