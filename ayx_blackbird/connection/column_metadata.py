class ColumnMetadata:
    def __init__(
        self,
        name,
        sdk_col_type,
        size=256,
        scale=0,
        source=None,
        description=None,
    ):
        self.name = name
        self.type = sdk_col_type
        self.size = size
        self.scale = scale
        self.source = source if source is not None else ""
        self.description = description if description is not None else ""