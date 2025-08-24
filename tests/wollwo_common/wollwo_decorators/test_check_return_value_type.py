"""
Copyright (c) ${YEAR} by Michal Perzel. All rights reserved.

License: MIT
"""

#: ------------------------------------------------ IMPORTS ------------------------------------------------
import sys
import os
import pytest
import re

from typing import Union, Any
from dataclasses import dataclass

#: Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from wollwo_decorators.check_return_value_type import CheckReturnValueType

#: ----------------------------------------------- VARIABLES -----------------------------------------------


#: ------------------------------------------------- CLASS -------------------------------------------------
@dataclass
class Test:
    a: Any

    @CheckReturnValueType(bool, use_annotation=True)
    def test_str(self) -> str:
        return self.a

    @CheckReturnValueType(bool, use_annotation=True)
    def test_bool_fallback(self):
        return self.a

    @CheckReturnValueType(None, use_annotation=False)
    def test_none_default(self):
        return self.a

    @CheckReturnValueType(str, use_annotation=True)
    def test_none_annotation(self) -> None:
        return self.a


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

    with pytest.raises(TypeError, match="Expected return type \"<class 'int'>\", got \"<class 'str'>\""):
        test('string')

    #: use_annotation=True
    @CheckReturnValueType(int, use_annotation=True)
    def test(a) -> Union[str, int]:
        return a

    result1 = test(000000)
    result2 = test('string')

    assert result1 == 000000
    assert result2 == 'string'

    with pytest.raises(TypeError, match=re.escape(
            "Expected return type \"typing.Union[str, int]\", got \"<class 'list'>\""
    )):
        test(['string', 000000])

    test = Test(123)

    with pytest.raises(TypeError, match='Expected return type "<class \'str\'>", got "<class \'int\'>"'):
        test.test_str()

    with pytest.raises(TypeError, match='Expected return type "<class \'bool\'>", got "<class \'int\'>"'):
        test.test_bool_fallback()

    with pytest.raises(TypeError, match='Expected return type "NoneType", got "<class \'int\'>"'):
        test.test_none_default()

    with pytest.raises(TypeError, match='Expected return type "NoneType", got "<class \'int\'>"'):
        test.test_none_annotation()


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

    with pytest.raises(TypeError, match=re.escape("Expected return type \"<class 'int'>\", got \"<class 'str'>\"")):
        with CheckReturnValueType(int) as crvt:
            crvt.check(test, 'string')

    with pytest.raises(TypeError, match=re.escape("Expected return type \"NoneType\", got \"<class 'str'>\"")):
        with CheckReturnValueType(None) as crvt:
            crvt.check(test, 'string')

    #: use_annotation=True
    with CheckReturnValueType(int, use_annotation=True) as crvt:
        result1 = crvt.check(test, 000000)
        result2 = crvt.check(test, 'string')

    assert result1 == 000000
    assert result2 == 'string'

    with pytest.raises(TypeError, match=re.escape(
            "Expected return type \"typing.Union[str, int]\", got \"<class 'list'>\""
    )):
        with CheckReturnValueType(int, use_annotation=True) as crvt:
            crvt.check(test, ['string', 000000])

#: ------------------------------------------------- BODY --------------------------------------------------
