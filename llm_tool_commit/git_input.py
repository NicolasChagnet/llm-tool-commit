import subprocess


def get_git_diff_raw() -> str:
    """Return the raw git diff from staged files."""
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    if result.returncode != 0:
        raise ValueError(f"Error running the command `git diff --cached`, return code: {result.returncode}")
    return result.stdout


def truncate_git_diff(git_diff: str, max_size: int) -> str:
    """Truncates the output from the git diff command if it is larger than the requested size."""
    max_size = min(max_size, len(git_diff))
    return git_diff[:max_size]


def set_git_commit(commit_message: str) -> None:
    """Set a commit with the given commit message."""
    result = subprocess.run(["git", "commit", "-m", '"commit_message"'])
    if result.returncode != 0:
        raise ValueError(
            f'Error running the command `git commit -m "{commit_message}"`, return code: {result.returncode}'
        )
