from collections import defaultdict
from typing import Any, Callable


class ObservableMixin:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event: Any, callback: Callable) -> None:
        self.subscribers[event].append(callback)

    def notify_topic(self, event: Any, payload: Any) -> None:
        for callback in self.subscribers[event]:
            callback(payload)
