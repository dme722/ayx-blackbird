"""Validator definitions."""
from typing import Any, Iterable, Type


def validate_object_type(val: Any, cls: Type) -> None:
    """Check that a value is an instance of a given class."""
    if not isinstance(val, cls):
        raise TypeError(f"Value {val} is not of type {str(cls)}")


def validate_iterable_of_type(val: Iterable[Any], cls: Type) -> None:
    """Validate that val is an iterable of objects of type cls."""
    for el in val:
        validate_object_type(el, cls)
