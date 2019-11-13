def validate_object_type(val, cls):
    """Check that a value is an instance of a given class."""
    if not isinstance(val, cls):
        raise TypeError(f"Value {val} is not of type {str(cls)}")


def validate_iterable_of_type(val, cls):
    for el in val:
        validate_object_type(el, cls)
