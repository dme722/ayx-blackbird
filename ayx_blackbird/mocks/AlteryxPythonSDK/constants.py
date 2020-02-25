"""SDK constants."""


class Status:
    """Status constants."""

    update_output_config_xml = 0


class EngineMessageType:
    """Engine output message types."""

    error = 100
    warning = 101
    info = 102


class FieldType:
    """SDK field types."""

    blob = "blob"
    byte = "byte"
    int16 = "int16"
    int32 = "int32"
    int64 = "int64"
    float = "float"
    double = "double"
    date = "date"
    time = "time"
    datetime = "datetime"
    bool = "bool"
    string = "string"
    v_string = "v_string"
    v_wstring = "v_wstring"
    wstring = "wstring"
    fixeddecimal = "fixeddecimal"
    spatialobj = "spatialobj"
