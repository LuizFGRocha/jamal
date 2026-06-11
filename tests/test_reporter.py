import json
from pathlib import Path

import pytest

from jamal.models import FileAnalysis
from jamal.reporter import Reporter


def _analysis(filename, changes=5, churn=100, complexity=3.0):
    return FileAnalysis(
        filename=filename,
        change_count=changes,
        total_churn=churn,
        avg_complexity=complexity,
        lines_of_code=80,
        function_count=5,
        authors={"Alice", "Bob"},
    )


def test_export_json(tmp_path):
    out = str(tmp_path / "out.json")
    Reporter().export_json({"total": 10, "items": []}, out)
    assert Path(out).exists()
    data = json.loads(Path(out).read_text(encoding="utf-8"))
    assert data["total"] == 10


def test_export_csv(tmp_path):
    out = str(tmp_path / "out.csv")
    Reporter().export_csv([_analysis("foo.py"), _analysis("bar.py")], out)
    content = Path(out).read_text(encoding="utf-8")
    assert "foo.py" in content
    assert "bar.py" in content
    assert "hotspot_score" in content


def test_export_csv_utf8_filename(tmp_path):
    out = str(tmp_path / "out.csv")
    Reporter().export_csv([_analysis("módulo/ação.py")], out)
    content = Path(out).read_text(encoding="utf-8")
    assert "módulo/ação.py" in content


def test_export_json_empty(tmp_path):
    out = str(tmp_path / "empty.json")
    Reporter().export_json({}, out)
    assert json.loads(Path(out).read_text(encoding="utf-8")) == {}


def test_export_csv_contains_all_columns(tmp_path):
    out = str(tmp_path / "cols.csv")
    Reporter().export_csv([_analysis("x.py")], out)
    header = Path(out).read_text(encoding="utf-8").splitlines()[0]
    for col in ["filename", "change_count", "total_churn", "avg_complexity", "bus_factor"]:
        assert col in header
