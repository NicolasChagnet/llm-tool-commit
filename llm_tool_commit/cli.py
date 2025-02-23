import click
from pydanclick import from_pydantic

from llm_tool_commit.config import ToolConfiguration


@click.command()
@from_pydantic(ToolConfiguration)
def entrypoint(config: ToolConfiguration):
    """Entry point of the CLI application."""
    pass
