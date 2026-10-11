"""Experiment 11: Power BI sales calculations and percentage analysis using DAX."""

from typing import Any, Optional
from .base import Experiment
from .exp10_powerbi_visualization import get_sales_data_path, load_sales_data

NUMBER = 11
TITLE = "Power BI Sales Calculations and DAX Measures"
CATEGORY = "Business Intelligence (Power BI)"
AIM = (
    "Using Power BI, perform sales calculation and percentage analysis using calculated "
    "columns and DAX measures."
)
DEPENDENCIES = ["Power BI Desktop", "sales_data.csv"]

CONCEPT = """\
Data Analysis Expressions (DAX) is the formula and query language utilized throughout Power BI:
- Calculated Columns: Evaluated row-by-row at model load/refresh time and materialized in RAM. \
Ideal for categorical classification and row-level computations:
  * Total Cost = Quantity * UnitCost
  * Profit = Sales - Total Cost
- DAX Measures: Dynamically evaluated at query time based on visual filter contexts:
  * Total Sales = SUM(Sales[Sales])
  * Total Profit = SUM(Sales[Profit])
  * Profit Margin % = DIVIDE([Total Profit], [Total Sales]) * 100
  * Sales % of Total = DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Sales))) * 100
  (CALCULATE with ALL overrides visual filters to obtain the grand total denominator).\
"""

CODE = """\
================================================================================
Experiment 11: Power BI Calculated Columns and DAX Measures
Tool: Microsoft Power BI Desktop
Source Data: sales_data.csv (Same table as Experiment 10)
================================================================================

1. CALCULATED COLUMNS (Modeling -> New Column)
   -----------------------------------------------------------------------------
   -- Column 1: Total Cost
   Total Cost = Sales[Quantity] * Sales[UnitCost]

   -- Column 2: Profit
   Profit = Sales[Sales] - Sales[Total Cost]

2. DAX MEASURES (Modeling -> New Measure)
   -----------------------------------------------------------------------------
   -- Measure 1: Total Sales
   Total Sales = SUM(Sales[Sales])

   -- Measure 2: Total Profit
   Total Profit = SUM(Sales[Profit])

   -- Measure 3: Profit Margin %
   Profit Margin % = DIVIDE([Total Profit], [Total Sales]) * 100

   -- Measure 4: Sales % of Total
   Sales % of Total = 
   DIVIDE(
       [Total Sales], 
       CALCULATE([Total Sales], ALL(Sales))
   ) * 100

3. REPORT VISUAL CONFIGURATION
   -----------------------------------------------------------------------------
   1. Table Visual:
      - Columns: Region, Total Sales, Total Profit, Profit Margin %, Sales % of Total
   2. Card Visuals:
      - Card 1: Total Sales (29,900)
      - Card 2: Total Profit (8,050)
   3. Clustered Bar Chart:
      - Y-axis (Category): Region
      - X-axis (Value): Sales % of Total
"""

EXPECTED_OUTPUT = """\
Expected Power BI Output Table:

+--------+-------------+--------------+-----------------+------------------+
| Region | Total Sales | Total Profit | Profit Margin % | Sales % of Total |
+--------+-------------+--------------+-----------------+------------------+
| East   |      10,000 |        2,800 |          28.00% |           33.44% |
| North  |       4,400 |        1,200 |          27.27% |           14.72% |
| South  |       4,400 |        1,200 |          27.27% |           14.72% |
| West   |      11,100 |        2,850 |          25.68% |           37.12% |
+--------+-------------+--------------+-----------------+------------------+
| Total  |      29,900 |        8,050 |          26.92% |          100.00% |
+--------+-------------+--------------+-----------------+------------------+

Card Visuals:
- Total Sales:  29,900
- Total Profit:  8,050
"""

RESULT = (
    "Calculated columns (Total Cost, Profit) and DAX measures (Total Sales, Total Profit, "
    "Profit Margin %, Sales % of Total) were successfully created and visualized in Power BI."
)

NOTES = """\
Pedagogical Notes:
- `DIVIDE()` is preferred over `/` because it handles divide-by-zero errors safely.
- `CALCULATE(..., ALL(Sales))` removes all filters from the Sales table to compute the global denominator.\
"""


def simulate_in_python() -> Any:
    """Simulate the DAX measures and calculated columns using pandas."""
    df = load_sales_data()
    df["Total Cost"] = df["Quantity"] * df["UnitCost"]
    df["Profit"] = df["Sales"] - df["Total Cost"]

    agg = df.groupby("Region", as_index=False).agg(
        {"Sales": "sum", "Profit": "sum"}
    ).rename(columns={"Sales": "Total Sales", "Profit": "Total Profit"})

    grand_sales = agg["Total Sales"].sum()
    grand_profit = agg["Total Profit"].sum()

    agg["Profit Margin %"] = (agg["Total Profit"] / agg["Total Sales"] * 100).round(2)
    agg["Sales % of Total"] = (agg["Total Sales"] / grand_sales * 100).round(2)

    total_row = {
        "Region": "Total",
        "Total Sales": grand_sales,
        "Total Profit": grand_profit,
        "Profit Margin %": round(grand_profit / grand_sales * 100, 2),
        "Sales % of Total": 100.00,
    }
    import pandas as pd
    return pd.concat([agg, pd.DataFrame([total_row])], ignore_index=True)


def run(show_simulation: bool = True) -> str:
    """Display DAX instructions and run Python validation simulation."""
    output = (
        "[Power BI Experiment 11 Notice]\n"
        "Power BI DAX expressions are evaluated inside Microsoft Power BI Desktop.\n\n"
        + CODE
        + "\n"
        + EXPECTED_OUTPUT
    )
    print(output)
    if show_simulation:
        try:
            print("\nPython Validation Simulation of DAX Logic:\n")
            sim = simulate_in_python()
            print(sim.to_string(index=False))
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
