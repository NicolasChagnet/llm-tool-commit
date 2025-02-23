def get_prompt(git_diff: str, length_git_commit: int) -> str:
    """Returns the prompt to feed the LLM.

    Args:
        git_diff (str): Truncated output of the `git diff --cached` command.
        length_git_commit (int): Maximal length in words of the commit message

    Returns:
        str: User prompt specifying the query.
    """

    return f"""Please summarize the changes made in the staged files from the output of the `git diff --cached` command placed between the XML tags <diff>. You must keep the response under {length_git_commit} words. Focus on why the changes were made. Place the summary inside <summary> XML tags.

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

    # Truncate the commit message if necessary
    truncated_commit = truncate_sentence(commit_message, max_words=message_max_length)
    return truncated_commit


def truncate_sentence(sentence: str, max_words: int) -> str:
    """Given a sentence, truncates it if it exceeds `max_words` and ensure it ends as a sentence."""
    sentence_split = sentence.split(" ")
    max_words = min(max_words, len(sentence_split))
    sentence_reconstructed = " ".join(sentence_split[:max_words])
    return sentence_reconstructed
