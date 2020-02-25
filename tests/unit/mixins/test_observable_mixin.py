from ayx_blackbird.mixins import ObservableMixin


def test_observability():
    observable = ObservableMixin()

    test_event_list = []
    all_events_list = []

    def test_event_callback(**kwargs):
        test_event_list.append(kwargs)

    def all_events_callback(**kwargs):
        all_events_list.append(kwargs)

    observable.subscribe("test_event", test_event_callback)
    observable.subscribe_all(all_events_callback)

    observable.notify_topic("test_event", payload="Hello from test event!")
    observable.notify_topic("surprise_event", surprise="New event!")

    assert len(test_event_list) == 1
    assert len(all_events_list) == 2
