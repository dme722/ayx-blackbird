from .column_metadata import ColumnMetadata

class ConnectionMetadata:
    @classmethod
    def build_from_record_info(cls, record_info):
        return cls([
                    ColumnMetadata(
                        field.name,
                        field.type,
                        size=field.size,
                        source=field.source,
                        scale=field.scale,
                        description=field.description,
                    )
                    for field in record_info
                ])

    def __init__(self, column_metadata=None):
        if column_metadata is None:
            column_metadata = []
        self.column_metadata = column_metadata
