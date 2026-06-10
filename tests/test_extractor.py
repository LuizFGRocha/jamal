import pytest

from jamal.extractor import Extractor
from jamal.models import FileMetrics


@pytest.fixture
def sample_py_file(tmp_path):
    py = tmp_path / "sample.py"
    py.write_text(
        "def add(a, b):\n"
        "    return a + b\n"
        "\n"
        "def factorial(n):\n"
        "    if n <= 1:\n"
        "        return 1\n"
        "    return n * factorial(n - 1)\n"
        "\n"
        "def classify(x):\n"
        "    if x > 0:\n"
        "        return 'positive'\n"
        "    elif x < 0:\n"
        "        return 'negative'\n"
        "    else:\n"
        "        return 'zero'\n"
    )
    return str(py)


def test_extract_known_file(sample_py_file):
    metrics = Extractor().extract(sample_py_file)
    assert isinstance(metrics, FileMetrics)
    assert metrics.function_count == 3
    assert metrics.lines_of_code > 0
    assert metrics.token_count > 0


def test_extract_complexity_positive(sample_py_file):
    metrics = Extractor().extract(sample_py_file)
    assert metrics.cyclomatic_complexity > 0


def test_extract_nonexistent_file():
    metrics = Extractor().extract("/nonexistent/path/file.py")
    assert metrics.cyclomatic_complexity == 0.0
    assert metrics.lines_of_code == 0
    assert metrics.function_count == 0


def test_extract_binary_file(tmp_path):
    binary = tmp_path / "data.bin"
    binary.write_bytes(b"\x00\x01\x02\x03\xff\xfe")
    metrics = Extractor().extract(str(binary))
    assert isinstance(metrics, FileMetrics)


def test_extract_empty_file(tmp_path):
    empty = tmp_path / "empty.py"
    empty.write_text("")
    metrics = Extractor().extract(str(empty))
    assert metrics.function_count == 0
    assert metrics.lines_of_code == 0
