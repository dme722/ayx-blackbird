"""Tool definition."""


class Tool:
    """Instance of a tool in a workflow along with associated data structures."""

    def __init__(self, engine, plugin_instance):
        """Construct a new tool object."""
        self.engine = engine
        self.plugin_instance = plugin_instance
        self.output_manager = None
        self.tool_id = None
