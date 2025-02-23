from unittest.mock import patch

import pytest

from llm_tool_commit.git_input import get_git_diff_raw, truncate_git_diff

MOCK_GIT_DIFF_CACHED = """
diff --git a/file1.py b/file1.py
index e69de29..b6fc4c9 100644
--- a/file1.py
+++ b/file1.py
@@ -0,0 +1,3 @@
+def hello_world():
+    print("Hello, world!")
+
diff --git a/file2.txt b/file2.txt
index e69de29..b6fc4c9 100644
--- a/file2.txt
+++ b/file2.txt
@@ -1 +1 @@
-Old content
+New content
"""
MOCK_GIT_DIFF_SHORTENED = "\ndiff --git a/file1.py b/file1.py\nindex "


def test_git_raw_code():
    """Tests the error handling of the function running the git subprocess."""
    with patch("subprocess.run") as mock_run:
        # Mock the subprocess
        mock_run.return_value.stdout = MOCK_GIT_DIFF_CACHED
        mock_run.return_value.returncode = 1

        with pytest.raises(ValueError):
            get_git_diff_raw()


def test_git_raw_output():
    """Tests the output of the function running the git subprocess."""
    with patch("subprocess.run") as mock_run:
        # Mock the subprocess
        mock_run.return_value.stdout = MOCK_GIT_DIFF_CACHED
        mock_run.return_value.returncode = 0

        output = get_git_diff_raw()
        assert output == MOCK_GIT_DIFF_CACHED, "Wrong output of the git diff subprocess"


def test_parse_git_raw():
    """Tests the processing function for the git diff output."""

    shortened_diff = truncate_git_diff(git_diff=MOCK_GIT_DIFF_CACHED, max_size=40)
    unshortened_diff = truncate_git_diff(git_diff=MOCK_GIT_DIFF_CACHED, max_size=300)
    assert shortened_diff == MOCK_GIT_DIFF_SHORTENED, "Issue when truncating a long git diff"
    assert unshortened_diff == MOCK_GIT_DIFF_CACHED, "Issue when truncating a short git diff"
