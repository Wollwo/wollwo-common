"""
Copyright (c) 2025 perzelmichal@gmail.com
All rights reserved.
"""
#: ------------------------------------------------ IMPORTS ------------------------------------------------
from dataclasses import dataclass, asdict, field, fields, MISSING
from typing import Optional, Union

#: ----------------------------------------------- VARIABLES -----------------------------------------------


#: ------------------------------------------------- CLASS -------------------------------------------------
@dataclass(init=True, repr=True, eq=True, order=True, frozen=False)
class Example:
    """
    Example Dataclass
    - shows how to set specialised __setattr__
    - how to set attributes
    - how to expect and use **kwargs

    Example:
         - creating instance with **kwargs:
             kwargs = {}

             @dataclass
             class Example:
                a: str

             e = Example(**{k.name: kwargs[k.name] for k in fields(Example) if k.name in kwargs})

    """
    one: str
    __two: dict = field(
        default_factory=lambda: {
            "example": "e_value",
            "info": "i_value"
        },
        init=False, repr=False
    )
    two: str = field(default='info')
    three: Optional[str] = field(default=None)
    four: Union[str, int] = field(default=0)

    #: Not visible
    __ten: Optional[object] = field(default=None, init=False, repr=False)

    def __post_init__(self, *args, **kwargs) -> None:
        """Post init tasks"""
        if hasattr(super(), '__post_init__'):
            super().__post__init__(*args, **kwargs)

        return

    def __setattr__(self, name, value):
        """Custom attribute setter"""

        attributes = {attr.name: attr.type for attr in fields(self)}

        #: Check provided types for all attributes, raise TypeError if there is no match
        if name in attributes.keys() and not isinstance(value, attributes[name]):
            raise TypeError(f'Expected "{name}" to be of type "{attributes[name]}", got {type(value).__name__}')

        #: If some attributes must have specific values
        if name == "two":
            value = value.lower()
            if value not in self.__two.keys():
                raise ValueError(f"Expected '{name}' to be in {list(self.__two.keys())}")

        super().__setattr__(name, value)


#: ------------------------------------------------ METHODS ------------------------------------------------


#: ------------------------------------------------- BODY --------------------------------------------------
if __name__ == '__main__':
    pass
