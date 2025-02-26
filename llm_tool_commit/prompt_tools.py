def get_system_prompt() -> str:
    """Returns the system prompt."""
    system_prompt = """You are a helpful assistant specialized in summarizing code diffs and crafting concise git commit messages. When writing a commit message, think carefully and write a summary in the format:
<summary>TYPE: SUMMARY</summary>
The TYPE parameter can be:
- 'feat' for changes involving new features, 
- 'fix' for small bugfixes,
- 'refactor' for changes which rewrite or restructure the code without changing the logic,
- 'perf' for changes aimed at improving performance,
- 'test' for changes adding, removing or modifying tests,
- 'docs' for changes affecting the documentation, comments or docstrings,
- 'build' for changes affecting the build system such as build tools, CI pipelines, dependencies, project version and manifest.

If the user does not specify a value for TYPE, choose one that matches the changes.
"""
    return system_prompt


def get_prompt(git_diff: str, length_git_commit: int, type_commit: str | None = None) -> str:
    """Returns the prompt to feed the LLM.

    Args:
        git_diff (str): Truncated output of the `git diff --cached` command.
        length_git_commit (int): Maximal length in words of the commit message
        type_commit (str): Type of commit to guide the LLM. Defaults to None.

    Returns:
        str: User prompt specifying the query.
    """
    type_commit_str = f"- Make sure to choose {type_commit} as value for TYPE" if type_commit is not None else ""
    return f"""Summarize the diff placed between the XML tags <diff>, following these guidelines:
    - You must keep the response under {length_git_commit} words. 
    - You must focus on why the changes were made.
    - Place the summary inside <summary> XML tags.
    {type_commit_str}
    
<diff>{git_diff}</diff>
"""


def parse_output(model_response: str, message_max_length: int) -> str:
    """Parses the response of the model to extract the commit message. Raises a ValueError if no XML `<summary>` tag can be found. Truncate the commit message

    Args:
        model_response (str): Response of the LLM.
        message_max_length (int): Maximal length of the commit message. The message will be automatically truncated above this.

    Returns:
        str: Commit message returned by the LLM.

    """
    if "<summary>" not in model_response or "</summary>" not in model_response:
        raise ValueError("No summary found in the model response.")

    # Extract the commit message from the response
    tag_name = "summary"
    position_begin = model_response.find(f"<{tag_name}>") + 2 + len(tag_name)
    position_end = model_response.find(f"</{tag_name}>")
    if position_begin > position_end:
        raise ValueError("Invalid placement of <summary> tags in the model response.")
    commit_message = model_response[position_begin:position_end]
    commit_message = clean_commit_message(commit_message)

    # Truncate the commit message if necessary
    truncated_commit = truncate_sentence(commit_message, max_words=message_max_length)
    return truncated_commit


def truncate_sentence(sentence: str, max_words: int) -> str:
    """Given a sentence, truncates it if it exceeds `max_words` and ensure it ends as a sentence."""
    sentence_split = sentence.split(" ")
    max_words = min(max_words, len(sentence_split))
    sentence_reconstructed = " ".join(sentence_split[:max_words])
    return sentence_reconstructed


def clean_commit_message(message: str) -> str:
    """Cleans the commit message by removing backticks and extra whitespaces."""

    message_no_backticks = message.replace("`", "'").replace('"', "'")
    message_no_whitespace = message_no_backticks.strip().replace("  ", " ")
    return message_no_whitespace
