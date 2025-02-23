def get_prompt(git_diff: str, length_git_commit: int) -> str:
    """Returns the prompt to feed the LLM.

    Args:
        git_diff (str): Truncated output of the `git diff --cached` command.
        length_git_commit (int): Maximal length in words of the commit message

    """

    return f"""Please summarize the changes made in the staged files from the output of the `git diff --cached` command placed between the XML tags <diff>. Keep your summary under {length_git_commit} words. Place the summary between XML <summary> tags. Write the summary in the conventional commit format if possible.

<diff>{git_diff}</diff>
"""


def parse_output(model_response: str, max_length_commit_message: int) -> str:
    """Parses the response of the model to extract the commit message. Raises a ValueError if no XML `<summary>` tag can be found. Truncate the commit message

    Args:
        model_response (str): Response of the LLM.
        max_length_commit_message (int): Maximal length of the commit message. The message will be automatically truncated above this.

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

    # Truncate the commit message if necessary
    truncation_point = min(len(commit_message), max_length_commit_message)
    return commit_message[:truncation_point]
