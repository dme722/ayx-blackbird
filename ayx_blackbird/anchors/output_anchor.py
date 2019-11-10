class OutputAnchor:
    def __init__(self, name, optional, engine_anchor_ref):
        self.name = name
        self.optional = optional
        self.num_connections = 0
        self._engine_anchor_ref = engine_anchor_ref

    def update_progress(self, percent):
        self._engine_anchor_ref.update_progress(percent)