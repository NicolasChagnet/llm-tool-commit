# LLM Tool Commit

## Summary

Simple CLI tool using a local LLM to analyze the staged changes diff and generating a commit message. This tool requires [ollama](https://ollama.com/) to be installed and running.


## Usage

```console
Usage: llm_tool_commit [OPTIONS]

  Entry point of the CLI application.

Options:
  --model TEXT                  Valid model on ollama
  --max-size-diff INTEGER       Maximal size of the diff before truncating
  --message-max-length INTEGER  Maximal size of the commit message in words
  --type-commit TEXT            Type of conventional commit to guide the model
  --temperature FLOAT           Temperature of the model (defaults to 0.4)
  --top-p FLOAT                 Defaults to 0.9
  --top-k INTEGER               Defaults to 40
  --num-predict INTEGER         Number of token to predict. Defaults to 2048.
  --help                        Show this message and exit.
  ```