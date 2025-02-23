import sys

import click
from ollama import generate
from pydanclick import from_pydantic

from llm_tool_commit.config import ModelOptions, ToolConfiguration
from llm_tool_commit.git_input import get_git_diff_raw, truncate_git_diff
from llm_tool_commit.prompt_tools import get_prompt, parse_output


@click.command()
@from_pydantic(ToolConfiguration)
@from_pydantic(ModelOptions)
def entrypoint(tool_configuration: ToolConfiguration, model_options: ModelOptions):
    """Entry point of the CLI application."""

    # Get the git diff of staged files
    git_diff = get_git_diff_raw()
    # Handle empty git diff
    if len(git_diff) == 0:
        click.echo("Empty `git diff`, nothing to do...")
        sys.exit(0)

    git_diff_truncated = truncate_git_diff(git_diff=git_diff, max_size=tool_configuration.max_size_diff)

    # Build prompt and query the LLM
    prompt = get_prompt(git_diff=git_diff_truncated, length_git_commit=tool_configuration.message_max_length)
    response = generate(model=tool_configuration.model, prompt=prompt, options=model_options.model_dump())
    response_content = response["response"]
    print(response_content)
    try:
        parsed_response = parse_output(response_content, message_max_length=tool_configuration.message_max_length)
        click.echo(parsed_response)
    except ValueError as error:
        click.echo(str(error))
        sys.exit(0)
