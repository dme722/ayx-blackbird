"""CLI implementation for ayx-blackbird package."""
import os
import shutil

import click

import xmltodict

name_to_tool = {
    "input": "BlackbirdInput",
    "multiple-inputs": "BlackbirdMultipleInputs",
    "multiple-outputs": "BlackbirdMultipleOutputs",
    "optional": "BlackbirdOptional",
    "output": "BlackbirdOutput",
    "passthrough": "BlackbirdPassthrough",
    "multianchor": "BlackbirdMultianchor",
}


@click.group()
def main() -> None:
    """Do nothing."""
    pass


@main.command()
@click.option("--name", help="Name of the tool to create", prompt="Tool Name: ")
@click.option(
    "--tool_directory",
    default="tools",
    help="Name of the top level tool directory to put this tool in.",
)
@click.option(
    "--tool_type",
    default="passthrough",
    help="The type of tool to create. "
    + "Must be one of: "
    + ", ".join(name_to_tool.keys()),
)
def create_ayx_plugin(name: str, tool_directory: str, tool_type: str) -> None:
    """Create a new plugin plugin for Alteryx Designer."""
    click.echo("Creating Alteryx Plugin...")

    try:
        example_tool_name = name_to_tool[tool_type]
    except KeyError:
        click.echo("tool_type must be one of: " + ", ".join(name_to_tool.keys()))
        return

    if not os.path.isdir(tool_directory):
        _setup_tool_dir(tool_directory)
        click.echo(f"Created tool directory: {os.path.abspath(tool_directory)}")

    new_tool_directory = os.path.abspath(os.path.join(tool_directory, name))
    if os.path.isdir(new_tool_directory):
        click.echo(
            f'Failed to create plugin: the plugin "{name}"'
            "already exists in {tool_directory}."
        )
        return

    click.echo(f"Created new tool in directory: {new_tool_directory}")

    _make_copy_of_example_tool(name, tool_directory, example_tool_name)
    _apply_name_change(name, example_tool_name, tool_directory)


def _setup_tool_dir(tool_directory: str) -> None:
    shutil.copytree(
        os.path.join(_get_install_dir(), "assets", "base_tool_config"), tool_directory
    )


def _make_copy_of_example_tool(
    new_tool_name: str, dest_dir: str, example_tool_name: str
) -> None:
    shutil.copytree(
        os.path.join(_get_install_dir(), "assets", "examples", example_tool_name),
        os.path.join(dest_dir, new_tool_name),
    )
    shutil.copy(
        os.path.join(_get_install_dir(), "assets", "examples", "requirements.txt"),
        os.path.join(dest_dir, new_tool_name, "requirements.txt"),
    )


def _get_install_dir() -> str:
    return os.path.dirname(os.path.realpath(__file__))


def _apply_name_change(name: str, example_tool_name: str, tool_directory: str) -> None:
    old_config_path = os.path.join(
        tool_directory, name, f"{example_tool_name}Config.xml"
    )
    new_config_path = _update_config_name(old_config_path, name)
    _update_name_in_config(new_config_path, name)
    _update_name_in_main_py(tool_directory, name, example_tool_name)


def _update_name_in_main_py(
    tool_directory: str, name: str, example_tool_name: str
) -> None:
    filepath = os.path.join(tool_directory, name, "main.py")
    with open(filepath, "r") as f:
        s = f.read()

    with open(filepath, "w") as f:
        s = s.replace(example_tool_name, name)
        f.write(s)


def _update_config_name(filepath: str, name: str) -> str:
    new_config_path = os.path.join(os.path.dirname(filepath), f"{name}Config.xml")
    os.rename(filepath, new_config_path)
    return new_config_path


def _update_name_in_config(config_filepath: str, name: str) -> None:
    with open(config_filepath) as f:
        config = xmltodict.parse(f.read())

    config["AlteryxJavaScriptPlugin"]["Properties"]["MetaInfo"]["Name"] = name

    with open(config_filepath, "w") as f:
        f.write(xmltodict.unparse(config, pretty=True))


@main.command()
@click.option(
    "--tool_path", default="tools", help="Path to the tool you want to install."
)
@click.option("--yxi_name", default="package", help="Name of the YXI file.")
@click.option("--destination_dir", default=".", help="Directory to put the YXI.")
def create_yxi(tool_path: str, yxi_name: str, destination_dir: str) -> None:
    """Create a YXI from a tools directory."""
    click.echo("Creating YXI...")

    yxi_path = os.path.join(destination_dir, yxi_name)
    shutil.make_archive(yxi_path, "zip", tool_path)

    shutil.move(f"{yxi_path}.zip", f"{yxi_path}.yxi")

    click.echo(f"Created YXI file at: {os.path.abspath(yxi_path)}.yxi")


if __name__ == "__main__":
    main()
