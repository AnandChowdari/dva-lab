# Experiment 12: Power BI Conditional and Logical Analysis (IF, AND, OR)

dax_logic = """
=== 1. Calculated Columns (Logical IF, AND, OR) ===
Sales Tier = IF(Sales[Sales] >= 3000, "High", IF(Sales[Sales] >= 2000, "Medium", "Low"))
High Value Order = IF(Sales[Sales] >= 3000 && Sales[Quantity] >= 5, "Yes", "No")
Furniture or Bulk = IF(Sales[Category] = "Furniture" || Sales[Quantity] >= 8, "Yes", "No")

=== 2. KPI Measures ===
High Tier Orders = CALCULATE(COUNTROWS(Sales), Sales[Sales Tier] = "High")
Electronics High Profit = CALCULATE([Total Profit], Sales[Category] = "Electronics", Sales[Profit] >= 1000)
"""

print(dax_logic)
