"""Exception definitions."""


class WorkflowRuntimeError(Exception):
    """Exception for a workflow runtime error."""


class AnchorNotFoundException(Exception):
    """Exception for when a requested anchor can't be found for the tool."""
