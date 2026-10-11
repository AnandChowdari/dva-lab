"""Experiment 12: Power BI conditional and logical analysis."""

from typing import Any, Optional
from .base import Experiment
from .exp10_powerbi_visualization import load_sales_data

NUMBER = 12
TITLE = "Power BI Conditional and Logical Analysis"
CATEGORY = "Business Intelligence (Power BI)"
AIM = (
    "Using Power BI, perform conditional and logical analysis using IF, AND, OR, "
    "and display totals and percentages using visualizations."
)
DEPENDENCIES = ["Power BI Desktop", "sales_data.csv"]

CONCEPT = """\
Conditional and boolean logic functions in DAX empower analysts to classify, segment, and \
filter records based on complex business criteria:
- Nested IF Statements: Classify tiered thresholds (e.g., Sales Level: High >= 5000, Medium >= 2500, Low < 2500).
- Boolean Conjunction (AND): Evaluates whether all conditions hold true simultaneously (e.g. Quantity >= 10 AND Region = 'East').
- Boolean Disjunction (OR): Evaluates whether at least one condition holds true (e.g. Region = 'West' OR Profit >= 1000).
- DAX Aggregations: COUNTROWS(Sales) counts orders while CALCULATE(..., ALL(Sales)) computes dynamic percentages.\
"""

CODE = """\
================================================================================
Experiment 12: Power BI Conditional and Logical Analysis (IF, AND, OR)
Tool: Microsoft Power BI Desktop
Source Data: sales_data.csv (With Profit column from Experiment 11)
================================================================================

1. CALCULATED COLUMNS (Modeling -> New Column)
   -----------------------------------------------------------------------------
   -- Column 1: Sales Level (Nested IF)
   Sales Level = 
   IF(Sales[Sales] >= 5000, "High",
      IF(Sales[Sales] >= 2500, "Medium", "Low"))

   -- Column 2: Bulk East Order (IF + AND)
   Bulk East Order = 
   IF(AND(Sales[Quantity] >= 10, Sales[Region] = "East"), "Yes", "No")

   -- Column 3: Focus Order (IF + OR)
   Focus Order = 
   IF(OR(Sales[Region] = "West", Sales[Profit] >= 1000), "Yes", "No")

2. DAX MEASURES (Modeling -> New Measure)
   -----------------------------------------------------------------------------
   -- Measure 1: Total Sales
   Total Sales = SUM(Sales[Sales])

   -- Measure 2: Order Count
   Order Count = COUNTROWS(Sales)

   -- Measure 3: Sales %
   Sales % = 
   DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Sales))) * 100

3. REPORT VISUAL CONFIGURATION
   -----------------------------------------------------------------------------
   1. Table Visual:
      - Columns: OrderID, Region, Sales, Sales Level, Bulk East Order, Focus Order
   2. Clustered Column Chart:
      - X-axis: Sales Level
      - Y-axis: Order Count
   3. Pie Chart:
      - Legend: Focus Order
      - Values: Total Sales (Show percentage data labels)
   4. Card Visuals:
      - Card 1: Total Sales (29,900)
      - Card 2: Order Count (10)
"""

EXPECTED_OUTPUT = """\
Expected Power BI Report Visual Outputs:

1. Sales Level Summary:
   +-------------+-------------+-------------+---------+
   | Sales Level | Order Count | Total Sales | Sales % |
   +-------------+-------------+-------------+---------+
   | High        |           1 |       5,600 |  18.73% |
   | Medium      |           4 |      15,400 |  51.51% |
   | Low         |           5 |       8,900 |  29.77% |
   +-------------+-------------+-------------+---------+
   | Total       |          10 |      29,900 | 100.00% |
   +-------------+-------------+-------------+---------+

2. Focus Order Summary:
   +-------------+-------------+-------------+---------+
   | Focus Order | Order Count | Total Sales | Sales % |
   +-------------+-------------+-------------+---------+
   | Yes         |           5 |      19,300 |  64.55% |
   | No          |           5 |      10,600 |  35.45% |
   +-------------+-------------+-------------+---------+
   | Total       |          10 |      29,900 | 100.00% |
   +-------------+-------------+-------------+---------+
"""

RESULT = (
    "Conditional and logical analysis using IF, AND, OR, along with totals and percentages, "
    "was successfully established and visualized in Power BI Desktop."
)

NOTES = """\
Logic Breakdown:
- Order 1 (Laptop East): Qty=5, Sales=4000, Profit=1000 -> Medium, Bulk East=No, Focus=Yes
- Order 2 (Phone West): Qty=10, Sales=4000, Profit=1000 -> Medium, Bulk East=No, Focus=Yes
- Order 5 (Tablet East): Qty=12, Sales=4200, Profit=1200 -> Medium, Bulk East=Yes, Focus=Yes
- Order 6 (Chair West): Qty=15, Sales=1500, Profit=450 -> Low, Bulk East=No, Focus=Yes
- Order 10 (Laptop West): Qty=7, Sales=5600, Profit=1400 -> High, Bulk East=No, Focus=Yes
Total Focus Orders = 5 (Total Sales = 19,300).\
"""


def simulate_in_python() -> Any:
    """Simulate Experiment 12 conditional and logical categorization using pandas."""
    df = load_sales_data()
    df["Total Cost"] = df["Quantity"] * df["UnitCost"]
    df["Profit"] = df["Sales"] - df["Total Cost"]

    # Calculated column: Sales Level
    def get_sales_level(val: float) -> str:
        if val >= 5000:
            return "High"
        elif val >= 2500:
            return "Medium"
        return "Low"

    df["Sales Level"] = df["Sales"].apply(get_sales_level)

    # Calculated column: Bulk East Order
    df["Bulk East Order"] = (
        (df["Quantity"] >= 10) & (df["Region"] == "East")
    ).map({True: "Yes", False: "No"})

    # Calculated column: Focus Order
    df["Focus Order"] = (
        (df["Region"] == "West") | (df["Profit"] >= 1000)
    ).map({True: "Yes", False: "No"})

    return df


def run(show_simulation: bool = True) -> str:
    """Display Power BI conditional logic tutorial and simulation results."""
    output = (
        "[Power BI Experiment 12 Notice]\n"
        "Power BI conditional reports are built inside Microsoft Power BI Desktop.\n\n"
        + CODE
        + "\n"
        + EXPECTED_OUTPUT
    )
    print(output)
    if show_simulation:
        try:
            print("\nPython Validation Simulation of IF / AND / OR Logic:\n")
            df = simulate_in_python()
            cols = ["OrderID", "Region", "Sales", "Sales Level", "Bulk East Order", "Focus Order"]
            print(df[cols].to_string(index=False))
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
