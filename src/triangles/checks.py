"""Module containing checks to be used elsewhere in the package."""

from typing import Any, Union, Type, Tuple


def check_type(
    obj: Any,
    expected_types: Union[Type, Tuple[Type]],
    obj_name: str,
    none_allowed: bool = False,
) -> None:
    """Function to check object is of given types and raise a TypeError if not.
    Parameters
    ----------
    obj : Any
        Any object to check the type of.
    expected_types : Union[Type, Tuple[Type]]
        Expected type or tuple of expected types of obj.
    none_allowed : bool = False
        Is None an allowed value for obj?
    """

    if type(expected_types) is tuple:

        if not all([type(expected_type) in [type] for expected_type in expected_types]):

            raise TypeError("all elements in expected_types must be types")

    else:

        if not type(expected_types) in [type]:

            raise TypeError("expected_types must be a type when passing a single type")

    if obj is None and not none_allowed:

        raise TypeError(f"{obj_name} is None and not is not allowed")

    elif obj is not None:

        if not isinstance(obj, expected_types):

            raise TypeError(
                f"{obj_name} is not in expected types {expected_types}, got {type(obj)}"
            )


def check_condition(condition: bool, error_message_text: str):
    """Check that condition (which evaluates to a bool) is True and raise a
    ValueError if not.
    Parameters
    ----------
    condition : bool
        Condition that evaluates to bool, to check.
    error_message_text : str
        Message to print in ValueError if condition does not evalute to True.
    """

    check_type(condition, bool, "condition")
    check_type(error_message_text, str, "error_message_text")

    if not condition:

        raise ValueError(f"condition: [{error_message_text}] not met")
