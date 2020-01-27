"""Constant definitions."""
from enum import Enum

NULL_VALUE_PLACEHOLDER = "BLACKBIRD_NULL_VALUE_PLACEHOLDER"


class ConnectionStatus(Enum):
    """Connection states."""

    CREATED = 0
    INITIALIZED = 1
    RECEIVING_RECORDS = 2
    CLOSED = 3
