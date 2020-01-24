class RecordProxy:
    __slots__ = ["ref", "creator"]

    def __init__(self, record_ref=None, record_creator=None):
        if record_ref is not None and record_creator is not None:
            raise RuntimeError(
                "Both record_ref and record_creator can't be simultaneously specified."
            )

        self.ref = None
        if record_ref is not None:
            self.ref = record_ref
        else:
            self.creator = record_creator

    @property
    def value(self):
        if self.ref is None:
            self.ref = self.creator.finalize_record()

        return self.ref
