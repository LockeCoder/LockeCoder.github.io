import json
from pathlib import Path


def test_notebook_contains_no_saved_output_or_embedded_password():
    p = Path(__file__).parents[1] / "ProjectTwoDashboard.ipynb"
    nb = json.loads(p.read_text(encoding="utf-8"))
    assert nb["nbformat"] == 4
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            assert cell["outputs"] == []
            assert cell["execution_count"] is None
    text = p.read_text()
    assert "PUT_A_STRONG_PASSWORD_HERE" not in text
    assert "codio.io" not in text
    assert "AnimalShelter.from_env" in text
