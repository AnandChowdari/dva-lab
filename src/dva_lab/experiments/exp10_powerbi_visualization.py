"""Experiment 10: Power BI sales data visualization."""

from pathlib import Path
from typing import Any, Optional
from .base import Experiment

NUMBER = 10
TITLE = "Power BI Sales Data Visualization"
CATEGORY = "Business Intelligence (Power BI)"
AIM = "Using Power BI, perform sales data visualization using predefined fields."
DEPENDENCIES = ["Power BI Desktop", "pandas (optional for dataset preview)"]

CONCEPT = """\
Power BI Desktop is an interactive business intelligence platform that transforms raw \
data tables into dynamic reports:
- Dimensional Slicing: Slicing metrics across spatial (Region), categorical (Category), and \
temporal (OrderDate) dimensions.
- Core Visualizations:
  * Clustered Column Chart: Compares total sales across regions.
  * Pie Chart: Visualizes categorical proportions (Electronics vs Furniture).
  * Line Chart: Highlights month-over-month sales trends.
  * Card Visual: Highlights top-level KPI summary metrics (e.g. Total Sales: 29,900).
  * Slicer: Enables interactive cross-filtering across the entire dashboard page.\
"""

CODE = """\
================================================================================
Experiment 10: Power BI Sales Data Visualization Using Predefined Fields
Tool: Microsoft Power BI Desktop
Source Data: sales_data.csv (10 rows)
================================================================================

1. DATA INGESTION
   - Launch Power BI Desktop.
   - On the Home ribbon, click 'Get data' -> 'Text/CSV'.
   - Select 'sales_data.csv' (located in dva_lab/data/sales_data.csv) and click 'Load'.
   - In the Data pane, verify table 'Sales' contains all columns:
     OrderID, OrderDate, Region, Category, Product, Quantity, UnitPrice, UnitCost, Sales

2. VISUAL 1: CLUSTERED COLUMN CHART (Sales by Region)
   - Visual Type: Clustered column chart
   - X-axis: Drag 'Region'
   - Y-axis: Drag 'Sales' (Aggregation: Sum)
   - Title: "Sum of Sales by Region"

3. VISUAL 2: PIE CHART (Sales by Category)
   - Visual Type: Pie chart
   - Legend: Drag 'Category'
   - Values: Drag 'Sales' (Aggregation: Sum)
   - Title: "Sum of Sales by Category"

4. VISUAL 3: LINE CHART (Monthly Sales Trend)
   - Visual Type: Line chart
   - X-axis: Drag 'OrderDate' (Set hierarchy to 'Month')
   - Y-axis: Drag 'Sales' (Aggregation: Sum)
   - Title: "Sales Trend by Month"

5. VISUAL 4: CARD (Overall KPI Metric)
   - Visual Type: Card
   - Fields: Drag 'Sales' (Displays total: 29.9K or 29,900)

6. VISUAL 5: SLICER (Interactive Regional Filter)
   - Visual Type: Slicer
   - Field: Drag 'Region'
   - Setting: Multi-select slicer to filter all visuals simultaneously.
"""

EXPECTED_OUTPUT = """\
Expected Power BI Report Visual Values:

1. Sum of Sales by Region:
   +--------+--------------+
   | Region | Sum of Sales |
   +--------+--------------+
   | East   |       10,000 |
   | North  |        4,400 |
   | South  |        4,400 |
   | West   |       11,100 |
   | Total  |       29,900 |
   +--------+--------------+

2. Sum of Sales by Category:
   +-------------+--------------+------------+
   | Category    | Sum of Sales | Percentage |
   +-------------+--------------+------------+
   | Electronics |       23,400 |     78.26% |
   | Furniture   |        6,500 |     21.74% |
   +-------------+--------------+------------+

3. Sum of Sales by Month:
   +----------+--------------+
   | Month    | Sum of Sales |
   +----------+--------------+
   | January  |        8,000 |
   | February |        3,200 |
   | March    |        5,700 |
   | April    |        5,600 |
   | May      |        7,400 |
   +----------+--------------+
"""

RESULT = (
    "Using Power BI Desktop, sales data visualizations (Clustered column, Pie, Line, "
    "Card, and Slicer) were successfully configured and verified."
)

NOTES = """\
Execution Guide:
- Power BI Desktop is a Windows application. Reports cannot be rendered purely in Python.
- Use `dva_lab.load_sales_data()` to inspect the exact dataset in Python or export to CSV.\
"""


def get_sales_data_path() -> Path:
    """Return the absolute path to sales_data.csv bundled in dva_lab."""
    return Path(__file__).resolve().parent.parent / "data" / "sales_data.csv"


def load_sales_data() -> Any:
    """Load and return the sales_data.csv as a pandas DataFrame."""
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "pandas is required to load the dataset into a DataFrame.\n"
            "Install with: pip install pandas"
        ) from exc
    return pd.read_csv(get_sales_data_path())


def run(show_preview: bool = True) -> str:
    """Display Power BI setup tutorial and dataset preview."""
    data_path = get_sales_data_path()
    output = (
        "[Power BI Experiment 10 Notice]\n"
        "Power BI reports are built inside Microsoft Power BI Desktop.\n"
        f"Bundled dataset location: {data_path}\n\n"
        + CODE
        + "\n"
        + EXPECTED_OUTPUT
    )
    if show_preview:
        print(output)
        try:
            df = load_sales_data()
            print("Dataset Preview (Top 5 rows):\n", df.head())
        except Exception:
            pass
    return CODE


def get_experiment() -> Experiment:
    """Create and return the Experiment instance."""
    return Experiment(
        number=NUMBER,
        title=TITLE,
        category=CATEGORY,
        aim=AIM,
        concept=CONCEPT,
        code=CODE,
        dependencies=DEPENDENCIES,
        expected_output=EXPECTED_OUTPUT,
        result=RESULT,
        notes=NOTES,
        run_func=run,
    )
