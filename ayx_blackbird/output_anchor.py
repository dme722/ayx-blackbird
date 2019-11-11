class OutputAnchor:
    def __init__(self, name, optional, engine_anchor_ref, record_info=None):
        self.name = name
        self.optional = optional
        self.num_connections = 0
        self._engine_anchor_ref = engine_anchor_ref
        self.metadata = None
        self.record_info = record_info

    def update_progress(self, percent):
        self._engine_anchor_ref.update_progress(percent)

    def push_metadata(self):
        if self.record_info is None:
            raise ValueError("record_info must be set before metadata can be pushed.")

        self._engine_anchor_ref.init(self.record_info)

    def push_records(self):
        # TODO
        pass

    def close(self):
        self._engine_anchor_ref.close()