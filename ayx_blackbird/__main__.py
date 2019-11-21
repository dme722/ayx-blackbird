import click


@click.command()
@click.option("--example-tool", default=False, help="Number of greetings.")
@click.option("--tool-name", help="The person to greet.")
def build_tool(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo("Hello %s!" % name)


if __name__ == "__main__":
    hello()
