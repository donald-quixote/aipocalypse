from enum import StrEnum
from typing import Any, Type
from neomodel import (StringProperty)

def enum_to_dict(enum_class):
    return {value.name: value.value for value in enum_class}

def enum_property(choices: Type[StrEnum], **kwargs: Any):
    return StringProperty(choices=enum_to_dict(choices), kwargs=kwargs)