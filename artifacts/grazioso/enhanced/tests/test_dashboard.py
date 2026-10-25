"""Dash initialization smoke test; runs when UI dependencies are installed."""
import pytest

pytest.importorskip("dash")
pytest.importorskip("dash_leaflet")

from dashboard_app import build_dashboard


def test_dash_layout_and_callbacks_register():
    class FakeRepository:
        pass
    app = build_dashboard(FakeRepository())
    assert app.layout is not None
    callbacks = " ".join(app.callback_map)
    for expected in ("datatable-id.data", "datatable-id.page_current", "graph-id.figure", "map-id.children"):
        assert expected in callbacks
