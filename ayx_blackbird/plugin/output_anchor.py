class OutputAnchor:
    def __init__(self, name, optional, engine_output_anchor_mgr, record_info=None, record_container=None):
        self.name = name
        self.optional = optional
        self.num_connections = 0
        self.record_info = record_info
        self.record_container = record_container

        self._engine_anchor_ref = engine_output_anchor_mgr.get_output_anchor(name)
        self._metadata_pushed = False

    def update_progress(self, percent):
        self._engine_anchor_ref.update_progress(percent)

    def push_metadata(self):
        if self.record_info is None:
            raise ValueError("record_info must be set before metadata can be pushed.")

        if not self._metadata_pushed:
            self._engine_anchor_ref.init(self.record_info)
            self._metadata_pushed = True

    def push_records(self):
        for record in self.record_container:
            self._engine_anchor_ref.push_record(record, False)

    def close(self):
        self._engine_anchor_ref.close()
