# CS-340 Project Two: Grazioso Salvare Dashboard

A Python dashboard project that connects a reusable MongoDB CRUD module to an interactive Dash/JupyterDash interface for filtering, visualizing, and mapping animal shelter records.

## Project Overview

This project was created for CS-340 to support Grazioso Salvare, an organization that identifies rescue dogs for specialized training programs.

The dashboard filters Austin Animal Center data based on rescue-type criteria and displays the matching records in multiple formats. Users can select a rescue profile, view matching animals in a data table, inspect breed distribution through a pie chart, and use an interactive map to view the selected animal's location.

This project demonstrates database-backed dashboard development, MongoDB query logic, reusable Python module design, interactive filtering, data visualization, and Jupyter Notebook-based application delivery.

## Repository Contents

- `ProjectTwoDashboard.ipynb` - Main Jupyter Notebook dashboard
- `CRUD_Python_Module.py` - Reusable MongoDB CRUD module
- `Grazioso Salvare Logo.png` - Dashboard logo asset
- `Project Two.docx` - Project documentation and write-up
- `.gitignore` - Git ignore configuration
- `README.md` - Repository documentation

## Features

- Connects a Python dashboard to MongoDB
- Uses a reusable CRUD module for database operations
- Filters animal records by rescue profile
- Displays matching records in an interactive data table
- Updates a pie chart based on filtered dashboard data
- Centers an interactive map on the selected animal record
- Includes reset functionality to return the dashboard to the starting state
- Separates database access logic from dashboard presentation logic

## Screenshots

1. **Starting state (Reset)**

<img width="623" height="317" alt="Picture1" src="https://github.com/user-attachments/assets/3d789747-d0d1-4e90-bafe-4138a67d4762" />

2. **Water Rescue applied**

<img width="624" height="318" alt="Picture2" src="https://github.com/user-attachments/assets/1149f054-0fba-4891-a9df-8e678daefc95" />

3. **Mountain/Wilderness applied**

<img width="622" height="321" alt="Picture3" src="https://github.com/user-attachments/assets/05083794-aa32-4064-80ee-9c77617c0670" />

4. **Disaster/Individual applied**

<img width="623" height="320" alt="Picture4" src="https://github.com/user-attachments/assets/1327ee0c-d5cc-498a-abfd-69b84d03ce80" />

5. **Reset again**

<img width="623" height="321" alt="Picture5" src="https://github.com/user-attachments/assets/54d5c956-5671-4ae3-81eb-1b63a279a40c" />

## Rescue Profile Filters

The dashboard includes filters for several rescue-training categories:

- Water Rescue
- Mountain or Wilderness Rescue
- Disaster or Individual Tracking
- Reset / All Records

Each filter applies specific criteria to the animal shelter dataset so users can narrow the results to dogs that may be suitable for the selected rescue role.

## Technologies Used

- Python
- MongoDB
- PyMongo
- Dash
- Plotly
- Jupyter Notebook
- JupyterDash
- Pandas
- Leaflet/map visualization
- Data filtering and visualization

## How to Run

### Requirements

- Python 3.x
- Jupyter Notebook or Codio/Jupyter environment
- MongoDB database access
- Required Python packages installed in the environment

### Run Instructions

1. Open `ProjectTwoDashboard.ipynb`.
2. Update database connection values if needed, including username, password, host, and port.
3. Run all notebook cells.
4. The dashboard should render inline through JupyterDash.
5. Use the dashboard controls to filter records, view table results, inspect the pie chart, and select records on the map.

If port `8050` is busy, use another available port:

```python
app.run_server(mode="inline", port=8051)
```

or:

```python
app.run_server(mode="inline", port=8052)
```

## MongoDB and CRUD Module

The project uses `CRUD_Python_Module.py` to separate database access from dashboard logic.

The CRUD module supports database connection handling and basic create, read, update, and delete operations against the animal shelter dataset. This separation improves maintainability because the dashboard interface, filtering rules, and database operations are not all mixed into one file.

This structure also makes the project easier to extend. Future dashboard features can reuse the CRUD module without rewriting database connection logic.

## Dashboard Workflow

1. The dashboard connects to MongoDB through the CRUD module.
2. Animal shelter records are loaded into the dashboard.
3. The user selects a rescue profile filter.
4. The data table updates to show matching records.
5. The pie chart updates to summarize the filtered data.
6. The map centers on the selected row from the table.
7. The reset option returns the dashboard to the default record view.

## Skills Demonstrated

- Python dashboard development
- MongoDB CRUD operations
- PyMongo database integration
- Interactive data filtering
- Dash and Plotly visualization
- Jupyter Notebook workflow
- Data-table updates
- Pie chart updates
- Interactive map updates
- UI-to-database integration
- Requirements-based implementation
- Technical documentation

## Project Value

This project shows the ability to connect a database-backed Python module to an interactive dashboard.

It demonstrates practical experience with MongoDB queries, dashboard callbacks, data filtering, and visualizing records in multiple formats for a specific user need. The project is strongest for roles involving software engineering, data dashboards, database-backed applications, QA/testing, application support, and Python-based development.

## Future Improvements

- Add a `requirements.txt` file for easier setup
- Add clearer MongoDB import and setup instructions
- Move supporting files into folders such as `notebooks/`, `src/`, `docs/`, and `assets/`
- Add more validation around missing or incomplete latitude/longitude data
- Add clearer error messages for failed database connections
- Add automated tests for CRUD module operations
- Add environment-variable support for database credentials

## Academic Portfolio Notice

This repository is shared as an academic portfolio artifact. It may include coursework documentation and assignment-specific material created for an educational setting.

Please do not reuse, submit, or redistribute this work as your own.
