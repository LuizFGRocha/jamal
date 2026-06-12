"""Shared pytest fixtures for Jamal tests."""

import subprocess

import pytest


@pytest.fixture(scope="session")
def fixture_repo(tmp_path_factory):
    """Create a temporary git repository with known commits for integration tests."""
    repo_dir = tmp_path_factory.mktemp("fixture_repo")

    def run(*args):
        subprocess.run(list(args), cwd=str(repo_dir), check=True, capture_output=True)

    run("git", "init")
    run("git", "config", "user.email", "test@example.com")
    run("git", "config", "user.name", "Test Author")

    main_py = repo_dir / "main.py"
    main_py.write_text(
        "def foo(x):\n"
        "    if x > 0:\n"
        "        return x\n"
        "    return -x\n"
        "\n"
        "def bar(a, b):\n"
        "    return a + b\n"
    )
    helper_py = repo_dir / "helper.py"
    helper_py.write_text("def greet(name):\n    return f'Hello, {name}'\n")

    run("git", "add", ".")
    run("git", "commit", "-m", "feat: initial commit")

    main_py.write_text(
        "def foo(x):\n"
        "    if x > 0:\n"
        "        return x\n"
        "    elif x == 0:\n"
        "        return 0\n"
        "    return -x\n"
        "\n"
        "def bar(a, b):\n"
        "    return a + b\n"
        "\n"
        "def baz(items):\n"
        "    return sum(items)\n"
    )
    run("git", "add", ".")
    run("git", "commit", "-m", "feat: extend foo and add baz")

    helper_py.write_text(
        "def greet(name):\n    return f'Hello, {name}'\n\n"
        "def farewell(name):\n    return f'Goodbye, {name}'\n"
    )
    run("git", "add", ".")
    run("git", "commit", "-m", "feat: add farewell to helper")

    return str(repo_dir)


@pytest.fixture
def big_commit_repo(tmp_path):
    """A repo with one oversized commit (>500 lines of churn)."""
    def run(*args):
        subprocess.run(list(args), cwd=str(tmp_path), check=True, capture_output=True)

    run("git", "init")
    run("git", "config", "user.email", "test@example.com")
    run("git", "config", "user.name", "Test Author")

    files = []
    for i in range(12):
        f = tmp_path / f"module_{i}.py"
        f.write_text("\n".join(f"def func_{j}(): pass" for j in range(50)))
        files.append(f"module_{i}.py")

    run("git", "add", ".")
    run("git", "commit", "-m", "chore: giant initial commit")
    return str(tmp_path)
