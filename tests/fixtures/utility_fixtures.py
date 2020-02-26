import os

from ayx_blackbird.config import ToolConfiguration

import pytest


@pytest.fixture
def tool_config_location_patch(monkeypatch):
    def patch(filename):
        monkeypatch.setattr(
            ToolConfiguration,
            "get_tool_config_filepath",
            lambda *args: os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), "..", "assets", "tool_configs", filename
                )
            ),
        )

    return patch
