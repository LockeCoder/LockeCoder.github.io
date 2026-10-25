"""Enhanced Grazioso Salvare dashboard: server-side MongoDB data operations.

The notebook and this standalone module use the same application and callbacks.
"""
from __future__ import annotations

import base64
import math
from pathlib import Path
from typing import Any

import dash_leaflet as dl
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html, dash_table

from CRUD_Python_Module import AnimalShelter, DataAccessError, DataValidationError
from rescue_filters import query_for, valid_coordinates


DISPLAY_FIELDS = [
    "animal_id", "name", "animal_type", "breed", "sex_upon_outcome",
    "age_upon_outcome_in_weeks", "outcome_type", "location_lat", "location_long",
]
HOME_COORDS = (30.75, -97.48)


def _logo_src() -> str | None:
    logo = Path(__file__).resolve().parent / "Grazioso Salvare Logo.png"
    if not logo.is_file():
        return None
    return "data:image/png;base64," + base64.b64encode(logo.read_bytes()).decode("ascii")


def _empty_map(message: str = "Select an animal to view its location"):
    return html.Div([
        html.P(message, role="status"),
        dl.Map(center=list(HOME_COORDS), zoom=9,
               style={"width": "100%", "height": "400px"}, children=[dl.TileLayer()]),
    ])


def build_dashboard(repository: AnimalShelter) -> Dash:
    """Create a Dash app using an injected repository for easy test isolation."""
    app = Dash(__name__, title="Grazioso Salvare | Rescue Dashboard")
    logo_src = _logo_src()
    app.layout = html.Div([
        html.Header([
            html.H1("Grazioso Salvare | Animal Rescue Dashboard"),
            html.Img(src=logo_src, alt="Grazioso Salvare logo",
                     style={"height": "110px"}) if logo_src else html.Div(),
            html.P("Explore Austin Animal Center animals by rescue suitability."),
        ], style={"textAlign": "center", "padding": "20px"}),
        html.Label("Rescue profile", htmlFor="filter-type"),
        dcc.RadioItems(id="filter-type", value="reset", inline=True, options=[
            {"label": "Water rescue", "value": "water"},
            {"label": "Mountain / wilderness rescue", "value": "mountain"},
            {"label": "Disaster / individual tracking", "value": "disaster"},
            {"label": "All animals", "value": "reset"},
        ]),
        html.Div(id="table-status", role="status", style={"padding": "12px 0"}),
        dash_table.DataTable(
            id="datatable-id",
            columns=[{"name": field.replace("_", " ").title(), "id": field}
                     for field in DISPLAY_FIELDS],
            data=[],
            page_action="custom",  # Database controls pagination, not Dash.
            page_current=0, page_size=10, page_count=1,
            sort_action="custom", sort_mode="single", sort_by=[],
            row_selectable="single", selected_rows=[],
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "7px", "minWidth": "110px"},
            style_header={"fontWeight": "bold"},
        ),
        html.Div([
            html.Div(dcc.Graph(id="graph-id"), style={"flex": "1", "minWidth": "300px"}),
            html.Div(id="map-id", style={"flex": "1", "minWidth": "300px"}),
        ], style={"display": "flex", "flexWrap": "wrap", "gap": "15px", "marginTop": "20px"}),
    ], style={"maxWidth": "1400px", "margin": "auto", "fontFamily": "Arial, sans-serif", "padding": "12px"})

    @app.callback(Output("datatable-id", "page_current"), Input("filter-type", "value"))
    def reset_page(_filter_type):
        return 0

    @app.callback(
        Output("datatable-id", "data"), Output("datatable-id", "page_count"),
        Output("table-status", "children"),
        Input("filter-type", "value"), Input("datatable-id", "page_current"),
        Input("datatable-id", "page_size"), Input("datatable-id", "sort_by"),
    )
    def update_table(filter_type, page_current, page_size, sort_by):
        query = query_for(filter_type)
        page_current = page_current or 0
        page_size = page_size or 10
        field, direction = "animal_id", 1
        if sort_by:
            field = sort_by[0]["column_id"]
            direction = -1 if sort_by[0].get("direction") == "desc" else 1
        try:
            result = repository.read_page(
                query, page=page_current, page_size=page_size, sort_field=field,
                sort_direction=direction, projection=DISPLAY_FIELDS,
            )
        except (DataAccessError, DataValidationError):
            return [], 1, "Database query failed. Check the connection and application logs."
        page_count = max(1, math.ceil(result.total / result.page_size))
        if not result.total:
            status = "No matching animals found."
        else:
            start = result.page * result.page_size + 1
            end = min(result.total, (result.page + 1) * result.page_size)
            status = f"Showing {start}–{end} of {result.total:,} matching animals."
        return result.documents, page_count, status

    @app.callback(Output("graph-id", "figure"), Input("filter-type", "value"))
    def update_graph(filter_type):
        try:
            rows = repository.aggregate_breed_distribution(query_for(filter_type))
        except (DataAccessError, DataValidationError):
            rows = []
        figure = go.Figure()
        if rows:
            figure.add_trace(go.Pie(
                labels=[row["breed"] for row in rows],
                values=[row["count"] for row in rows],
                hole=0.30,
            ))
        else:
            figure.add_annotation(text="No summary data available", showarrow=False)
        figure.update_layout(title="Top breeds among all matching animals", height=425)
        return figure

    @app.callback(Output("map-id", "children"),
                  Input("datatable-id", "data"), Input("datatable-id", "selected_rows"))
    def update_map(rows: list[dict] | None, selected_rows: list[int] | None):
        if not rows:
            return _empty_map("No animal location is available.")
        index = (selected_rows or [0])[0]
        if type(index) is not int or index < 0 or index >= len(rows):
            index = 0
        row = rows[index]
        position = valid_coordinates(row)
        if position is None:
            return _empty_map("This animal has no valid coordinates.")
        lat, lon = position
        details = f"{row.get('name') or 'Unnamed animal'} — {row.get('breed') or 'Unknown breed'}"
        return dl.Map(center=[lat, lon], zoom=11,
                      style={"width": "100%", "height": "400px"}, children=[
                          dl.TileLayer(),
                          dl.Marker(position=[lat, lon], children=[dl.Tooltip(details)]),
                      ])

    return app


def main():
    database = AnimalShelter.from_env()
    import os
    if os.getenv("MONGO_CREATE_INDEXES", "0") == "1":
        database.ensure_indexes()
    app = build_dashboard(database)
    host = os.getenv("DASH_HOST", "127.0.0.1")
    port = int(os.getenv("DASH_PORT", "8051"))
    # Expose externally only when the operator explicitly configures DASH_HOST.
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
