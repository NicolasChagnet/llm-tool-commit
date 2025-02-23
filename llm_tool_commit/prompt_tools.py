CONVENTIONAL_COMMIT = """
<type>: <description>

Possible <types> and commits they describe:

- feat: Commits that add or remove a new feature to the API or UI
- fix: Commits that fix a API or UI bug of a preceded feat commit
- refactor: Commits that rewrite/restructure your code, however do not change any API or UI behaviour
- perf: Special refactor commits, that improve performance
- style: Commits that do not affect the meaning (white-space, formatting, missing semi-colons, etc)
- test: Commits that add missing tests or correcting existing tests
- docs: Commits that affect documentation only
- build: Commits that affect build components like build tool, ci pipeline, dependencies, project version, ...
- ops: Commits that affect operational components like infrastructure, deployment, backup, recovery, ...
- chore: Miscellaneous commits e.g. modifying .gitignore
"""


def get_prompt(git_diff: str, length_git_commit: int, type_commit: str | None = None) -> str:
    """Returns the prompt to feed the LLM.

    Args:
        git_diff (str): Truncated output of the `git diff --cached` command.
        length_git_commit (int): Maximal length in words of the commit message
        type_commit (str): Type of commit to guide the LLM. Defaults to None.

    Returns:
        str: User prompt specifying the query.
    """
    type_commit_str = f"Make sure to choose {type_commit} as <type>" if type_commit is not None else ""
    return f"""Summarize the changes made in the staged files from the output of the `git diff --cached` command placed between the XML tags <diff>, following these guidelines:
    - You must keep the response under {length_git_commit} words. 
    - You must focus on why the changes were made.
    - Place the summary inside <summary> XML tags.
    - Follow the conventional commit format defined between the XML tags <format>.
    
<format>{CONVENTIONAL_COMMIT}</format>    

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

    message_no_backticks = message.replace("`", "'")
    message_no_whitespace = message_no_backticks.strip().replace("  ", " ")
    return message_no_whitespace
