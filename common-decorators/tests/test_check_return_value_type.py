"""
Copyright (c) 2025 perzelmichal@gmail.com
All rights reserved.
"""
#: ------------------------------------------------ IMPORTS ------------------------------------------------
import sys
import os
import pytest
import re

from typing import Union

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from common_decorators.check_return_value_type import CheckReturnValueType

#: ----------------------------------------------- VARIABLES -----------------------------------------------


#: ------------------------------------------------- CLASS -------------------------------------------------


#: ------------------------------------------------ METHODS ------------------------------------------------
def test_checkreturnvaluetype_class_as_decorator():
    """
    testing CheckReturnValueType
    """
    #: use_annotation=False
    @CheckReturnValueType(int)
    def test(a) -> Union[str, int]:
        return a

    result1 = test(000000)
    assert result1 == 000000

    with pytest.raises(TypeError, match="Expected return type <class 'int'>, got <class 'str'>"):
        test('string')

    #: use_annotation=True
    @CheckReturnValueType(int, use_annotation=True)
    def test(a) -> Union[str, int]:
        return a

    result1 = test(000000)
    result2 = test('string')

    assert result1 == 000000
    assert result2 == 'string'

    with pytest.raises(TypeError, match=re.escape("Expected return type typing.Union[str, int], got <class 'list'>")):
        test(['string', 000000])


def test_checkreturnvaluetype_class_as_contextmanager():
    """
    testing CheckReturnValueType
    """
    def test(a) -> Union[str, int]:
        return a

    #: use_annotation=False
    with CheckReturnValueType(int) as crvt:
        result1 = crvt.check(test, 000000)
    assert result1 == 000000

    with pytest.raises(TypeError, match=re.escape("Expected return type <class 'int'>, got <class 'str'>")):
        with CheckReturnValueType(int) as crvt:
            crvt.check(test, 'string')

    #: use_annotation=True
    with CheckReturnValueType(int, use_annotation=True) as crvt:
        result1 = crvt.check(test, 000000)
        result2 = crvt.check(test, 'string')

    assert result1 == 000000
    assert result2 == 'string'

    with pytest.raises(TypeError, match=re.escape("Expected return type typing.Union[str, int], got <class 'list'>")):
        with CheckReturnValueType(int, use_annotation=True) as crvt:
            crvt.check(test, ['string', 000000])

#: ------------------------------------------------- BODY --------------------------------------------------
