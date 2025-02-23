from click.testing import CliRunner

from llm_tool_commit.cli import entrypoint


def test_exit_code_help():
    """Test that the CLI app returns a successful exit code on calling help."""
    runner = CliRunner()
    result = runner.invoke(entrypoint, "--help")
    assert result.exit_code == 0
