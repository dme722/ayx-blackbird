import os
import shutil

import click

import xmltodict

example_tool_name = "BlackbirdExample"


@click.group()
def main():
    pass


@main.command()
@click.option("--name", default=example_tool_name, help="Name of the tool to create")
@click.option(
    "--tool_directory",
    default="tools",
    help="Name of the top level tool directory to put this tool in.",
)
def create_ayx_plugin(name, tool_directory):
    click.echo("Creating Alteryx Plugin...")

    if not os.path.isdir(tool_directory):
        setup_tool_dir(tool_directory)

    if os.path.isdir(os.path.join(tool_directory, name)):
        click.echo(
            f'Failed to create plugin: the plugin "{name}" already exists in {tool_directory}.'
        )
        return

    make_copy_of_example_tool(name, tool_directory)
    apply_name_change(name, tool_directory)


def setup_tool_dir(tool_directory):
    shutil.copytree(
        os.path.join(get_install_dir(), "assets", "base_tool_config"), tool_directory
    )


def make_copy_of_example_tool(new_tool_name, dest_dir):
    shutil.copytree(
        os.path.join(get_install_dir(), "Examples", example_tool_name),
        os.path.join(dest_dir, new_tool_name),
    )


def get_install_dir():
    return os.path.dirname(os.path.realpath(__file__))


def apply_name_change(name, tool_directory):
    old_config_path = os.path.join(
        tool_directory, name, f"{example_tool_name}Config.xml"
    )
    new_config_path = update_config_name(old_config_path, name)
    update_name_in_config(new_config_path, name)
    update_name_in_main_py(tool_directory, name)


def update_name_in_main_py(tool_directory, name):
    filepath = os.path.join(tool_directory, name, "main.py")
    with open(filepath, "r") as f:
        s = f.read()

    with open(filepath, "w") as f:
        s = s.replace(example_tool_name, name)
        f.write(s)


def update_config_name(filepath, name):
    new_config_path = os.path.join(os.path.dirname(filepath), f"{name}Config.xml")
    os.rename(filepath, new_config_path)
    return new_config_path


def update_name_in_config(config_filepath, name):
    with open(config_filepath) as f:
        config = xmltodict.parse(f.read())

    config["AlteryxJavaScriptPlugin"]["Properties"]["MetaInfo"]["Name"] = name

    with open(config_filepath, "w") as f:
        f.write(xmltodict.unparse(config, pretty=True))


@main.command()
@click.option("--tool_path", help="Path to the tool you want to install.")
@click.option(
    "--create_venv",
    default=True,
    help="Create the virtual environment and install requirements.txt.",
)
@click.option(
    "--admin",
    default=False,
    help="Create the virtual environment and install requirements.txt.",
)
def install(tool_path, create_venv):
    click.echo("TODO: Installing to Alteryx Designer...")


@main.command()
@click.option(
    "--tool_path", default="tools", help="Path to the tool you want to install."
)
@click.option("--yxi_name", default="package", help="Name of the YXI file.")
@click.option("--destination_dir", default=".", help="Directory to put the YXI.")
def create_yxi(tool_path, yxi_name, destination_dir):
    click.echo("Creating YXI...")

    yxi_path = os.path.join(destination_dir, yxi_name)
    shutil.make_archive(yxi_path, "zip", tool_path)

    shutil.move(f"{yxi_path}.zip", f"{yxi_path}.yxi")


if __name__ == "__main__":
    main()
