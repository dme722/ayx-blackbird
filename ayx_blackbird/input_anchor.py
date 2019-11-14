class InputAnchor:
    def __init__(self, name: str, optional: bool):
        self.name = name
        self.optional = optional
        self.connections = []
