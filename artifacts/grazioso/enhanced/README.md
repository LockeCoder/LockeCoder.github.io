# Grazioso Salvare — CS 499 Enhanced Database Artifact

This enhanced version of my CS 340 Grazioso Salvare project implements the database improvements planned in my CS 499 code-review narration. It retains rescue-profile selection, a paginated animal table, a breed-distribution chart, and an interactive map, while separating database logic from presentation.

## What changed from the original

| Enhancement | Implementation |
|---|---|
| Server-side filtering, sorting, projections, pagination | `AnimalShelter.read_page()` uses MongoDB `count_documents`, `find`, `sort`, `skip`, and `limit`; the Dash table uses `page_action="custom"` and `sort_action="custom"`. |
| Database indexes | Explicit `ensure_indexes()` creates indexes on frequently filtered rescue fields and on `animal_id`. |
| Aggregation | `aggregate_breed_distribution()` runs a MongoDB `$match`/`$group`/`$sort`/`$limit` pipeline, summarizing **all matching records**, not only the visible page. |
| Input validation | Approved field and operator allowlists, bounded page sizes, restricted update operators, and nonempty filters for update/delete. |
| Environment-based configuration | `AnimalShelter.from_env()` reads MongoDB URI, credentials, and connection settings from environment variables instead of notebook source code. |
| Explicit failures | `DataValidationError` and `DataAccessError` distinguish invalid requests, connectivity failures, and valid empty results. |
| Dashboard reliability | Controlled MongoDB paging; empty-result messaging; nonfinite/out-of-range geocoordinates rejected; saved notebook output and old Codio proxy links removed. |
| Automated tests | `pytest` coverage for validation, pagination and MongoDB call arguments, aggregation, index definitions, CRUD handling, rescue profiles, coordinates, and notebook hygiene; optional real MongoDB integration test. |

## Files

- `CRUD_Python_Module.py` — validated, indexed, paginated MongoDB data-access layer.
- `rescue_filters.py` — unchanged rescue-profile criteria extracted for reuse and testing.
- `dashboard_app.py` — reusable Dash application, database-backed custom paging and server-generated charts.
- `ProjectTwoDashboard.ipynb` — clean Jupyter entry point for the enhanced app.
- `Grazioso Salvare Logo.png` — existing dashboard brand asset.
- `.env.example` — configuration examples, **not** live credentials.
- `.gitignore` — excludes real `.env`, virtual environments and notebook checkpoints.
- `requirements.txt` and `requirements-dev.txt` — installation dependencies.
- `tests/` — automated tests.

## Install and run

Prerequisites: Python 3.10+, reachable MongoDB, and the **Austin Animal Center dataset** imported into `aac.animals` (not distributed here).

```bash
python -m venv .venv
# Activate your virtual environment before continuing.
python -m pip install -r requirements.txt
```

Provide your connection settings through operating-system environment variables. **Do not place passwords or real connection URIs in GitHub.** Examples:

```bash
# Local unauthenticated MongoDB for development ONLY:
export MONGO_HOST=localhost
export MONGO_PORT=27017
export MONGO_DB=aac
export MONGO_COLLECTION=animals

# For authenticated MongoDB, set a MONGO_URI in your private environment
# or set both MONGO_USERNAME and MONGO_PASSWORD privately.
```

Start the standalone dashboard:

```bash
python dashboard_app.py
```

Or open `ProjectTwoDashboard.ipynb` from this same directory and run the cells. Dash >= 2.17 provides Jupyter inline support directly.

### Index creation

If your database user has index-management privileges, explicitly enable index creation before starting the dashboard:

```bash
export MONGO_CREATE_INDEXES=1
```

Alternatively, call `AnimalShelter.from_env().ensure_indexes()` in a trusted administrative session. Existing records are not modified by index creation. Setting this variable is optional; the dashboard remains functional without creating indexes.

### Automated tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
```

The optional real MongoDB integration test requires `TEST_MONGO_URI`, which should point to a **disposable, isolated test instance**; the test creates and drops the `grazioso_capstone_tests` database. Never run it on a shared or production MongoDB server.

## Security and behavioral notes

- The original project remains in `../Original/`; the original notebook's saved Codio output is not carried into the enhanced notebook.
- `create`, `update`, and `delete` are available in the database module but **not exposed as unauthenticated dashboard UI actions**.
- The dashboard reads all matching documents only when explicitly calling the backward-compatible `read()` method; its own data path uses `read_page()` and bounded aggregation results.
- No live credentials, production database, or production deployment are included in this repository.
- This is academic portfolio source code. Local tests and any later GitHub Actions results should be recorded separately from claims of a deployed production application.
