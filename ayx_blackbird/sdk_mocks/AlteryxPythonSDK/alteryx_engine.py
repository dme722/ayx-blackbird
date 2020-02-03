"""Mock alteryx engine class definition."""


class AlteryxEngine:
    """Alteryx Engine mock."""

    def create_temp_file_name(self, extension: str = "tmp", options: int = 0) -> str:
        """Create temp file."""
        raise NotImplementedError()

    def decrypt_password(self, encrypted_password: str, mode: int) -> str:
        raise NotImplementedError()

    def get_constant(self, tool_id: int, which: int) -> None:
        raise NotImplementedError()

    def get_init_var(self, tool_id: int, var_name: str) -> str:
        raise NotImplementedError()

    def output_message(self, tool_id: int, status: int, message: str) -> int:
        raise NotImplementedError()

    def output_tool_progress(self, tool_id: int, percent_progress: float) -> int:
        raise NotImplementedError()

    def pre_sort(
        self,
        incoming_connection_type: str,
        incoming_connection_name: str,
        sort_info: str,
    ) -> None:
        raise NotImplementedError()
