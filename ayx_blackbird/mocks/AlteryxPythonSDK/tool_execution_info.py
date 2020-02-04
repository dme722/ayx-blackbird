from typing import List, Optional


class ToolExecutionInfo:
    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.infos: List[str] = []
        self.output_workflow_xml: Optional[str] = None

    def add_error(self, error: str) -> None:
        self.errors.append(error)

    def add_warning(self, warning: str) -> None:
        self.warnings.append(warning)

    def add_info(self, info: str) -> None:
        self.infos.append(info)

    def set_output_workflow_xml(self, xml: str) -> None:
        self.output_workflow_xml = xml
