from pathlib import Path


def test_pyproject_declares_quality_gate_dependencies_and_config():
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")

    assert '"ruff' in pyproject
    assert '"mypy' in pyproject
    assert '"pytest-cov' in pyproject
    assert "[tool.ruff]" in pyproject
    assert "[tool.mypy]" in pyproject
    assert "[tool.pytest.ini_options]" in pyproject


def test_ci_runs_lint_typecheck_and_coverage():
    ci = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "ruff check" in ci
    assert "mypy" in ci
    assert "--cov=geoserver_mcp" in ci
