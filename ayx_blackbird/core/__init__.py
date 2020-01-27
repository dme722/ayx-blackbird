"""Core class definitions."""
from .base_plugin import BasePlugin
from .connection_callback_strategy import ConnectionCallbackStrategy
from .connection_interface import ConnectionInterface
from .events import ConnectionEvents, PluginEvents

__all__ = [
    "BasePlugin",
    "ConnectionCallbackStrategy",
    "ConnectionInterface",
    "ConnectionEvents",
    "PluginEvents",
]
