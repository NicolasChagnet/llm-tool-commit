import pytest

from llm_tool_commit.prompt_tools import parse_output, truncate_sentence

COMMIT_MSG = """fix(api): handle empty response from server

- Added check for empty response in `fetchData` function
- Updated error handling to provide more informative messages
"""

COMMIT_MSG_TRUNCATED = "fix(api): "

OUTPUT_MODEL_1 = """
Certainly, here is a summary of the changes made in the staged files.

<summary>fix(api): handle empty response from server

- Added check for empty response in `fetchData` function
- Updated error handling to provide more informative messages
</summary>
Is there anything else I can help you with?
"""

OUTPUT_MODEL_2 = """
Certainly, here is a summary of the changes made in the staged files.

fix(api): handle empty response from server

- Added check for empty response in `fetchData` function
- Updated error handling to provide more informative messages

Is there anything else I can help you with?
"""

OUTPUT_MODEL_3 = """
Certainly, here is a summary of the changes made in the staged files.

<summary>fix(api): handle empty response from server

- Added check for empty response in `fetchData` function
- Updated error handling to provide more informative messages

Is there anything else I can help you with?
"""


def test_parse_output():
    """Tests the extraction of the summary from the XML tags"""
    commit_msg = parse_output(OUTPUT_MODEL_1, message_max_length=1000)
    print(commit_msg)
    assert commit_msg == COMMIT_MSG, "Issue when extract the commit message from the model output"


def test_parse_output_truncated():
    """Tests the truncation of the extracted summary."""
    commit_msg = parse_output(OUTPUT_MODEL_1, message_max_length=10)
    assert (
        commit_msg == COMMIT_MSG_TRUNCATED
    ), "Issue when truncating the extracted commit message from the model output"


def test_parse_output_missing_both_xml():
    """Tests the error handling when the XML tags are both missing"""
    with pytest.raises(ValueError):
        (
            parse_output(OUTPUT_MODEL_2, message_max_length=1000),
            "Issue when checking for raised error due to both summary tags missing",
        )


def test_parse_output_missing_one_xml():
    """Tests the error handling when one of the XML tags is missing"""
    with pytest.raises(ValueError):
        (
            parse_output(OUTPUT_MODEL_3, message_max_length=1000),
            "Issue when checking for raised error due to one missing summary tag",
        )


def test_truncate_sentence():
    assert truncate_sentence("This is an example of a sentence", 5) == "This is an example of"
    assert truncate_sentence("This is an example of a sentence", 8) == "This is an example of a sentence"
