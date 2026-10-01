import pathlib
import subprocess
from typing import Tuple
from langchain_core.tools import tool

PROJECT_ROOT = pathlib.Path.cwd() / "generated_project"

def safe_path_for_project(path: str) -> pathlib.Path:
    root = PROJECT_ROOT.resolve()
    p = (PROJECT_ROOT / path).resolve()
    if p != root and root not in p.parents:
        raise ValueError("Attempt to write outside project root")
    return p

@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return f"WROTE:{p}"


@tool
def read_file(path: str) -> str:
    """Reads content from a file at the specified path within the project root."""
    try:
        p = safe_path_for_project(path)
    except ValueError as e:
        return f"ERROR: {e}"
    if not p.exists():
        return ""
    if p.is_dir():
        return ""
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


@tool
def get_current_directory() -> str:
    """Returns the current working directory."""
    return str(PROJECT_ROOT)

IGNORE_DIRS = {".venv","venv","__pycache__","node_modules",".git",".idea"}

@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory within the project root."""
    try:
        p = safe_path_for_project(directory)
    except ValueError as e:
        return f"ERROR: {e}"
    if not p.is_dir():
        return f"ERROR: {p} is not a directory"
    files = [str(f.relative_to(PROJECT_ROOT)) for f in p.glob("**/*") if f.is_file() and not any(part in IGNORE_DIRS for part in f.parts)]
    return "\n".join(files) if files else "No files found."

@tool
def run_cmd(cmd: str, cwd: str = ".", timeout: int = 30) -> Tuple[int, str, str]:
    """Runs a shell command in the specified directory and returns the result."""
    cwd_dir = PROJECT_ROOT/cwd
    res = subprocess.run(cmd, shell=True, cwd=str(cwd_dir), capture_output=True, text=True, timeout=timeout)
    return res.returncode, res.stdout, res.stderr


def init_project_root():
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT)

def has_git_remote(remote_name: str = "origin") -> bool:
    result = subprocess.run(
        f"git remote get-url {remote_name}",
        shell=True,
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def auto_git_push(message : str):
    if not has_git_remote():
        return False, "No 'origin' remote configured on generated_project — skipping push."
    commands = [
        "git add .",
        f'git commit -m "{message}"',
        "git push origin main"
    ]

    for cmd in commands:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return False, result.stderr
    return True, "Git push successful."