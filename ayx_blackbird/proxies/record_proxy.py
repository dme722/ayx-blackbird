class RecordProxy:
    __slots__ = ["_ref", "_creator"]

    def __init__(self, record_ref=None, record_creator=None):
        if record_ref is not None and record_creator is not None:
            raise RuntimeError("Both record_ref and record_creator can't be simultaneously specified.")

        self._ref = None
        if record_ref is not None:
            self._ref = record_ref
        else:
            self._creator = record_creator

    @property
    def value(self):
        if self._ref is None:
            self._ref = self._creator.finalize_record()

        return self._ref
