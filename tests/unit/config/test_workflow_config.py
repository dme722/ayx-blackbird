from ayx_blackbird.config import WorkflowConfiguration

import xmltodict


def test_workflow_config_construction():
    config = {"Configuration": {"Test": "Config", "Value": "123"}}

    data = config["Configuration"]

    config_str = xmltodict.unparse(
        config, full_document=False, short_empty_elements=True
    )

    workflow_config = WorkflowConfiguration(config_str)

    assert workflow_config.data == data
    assert workflow_config.original_data == data
    assert workflow_config.data is not workflow_config.original_data

    workflow_config["Value"] = 456
    assert workflow_config.data["Value"] == 456
    assert workflow_config.original_data["Value"] == data["Value"]
