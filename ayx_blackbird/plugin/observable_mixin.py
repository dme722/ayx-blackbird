from collections import defaultdict


class ObservableMixin:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, topic, callback):
        self.subscribers[topic].append(callback)

    def notify_topic(self, topic, payload):
        for callback in self.subscribers[topic]:
            callback(payload)
