# Experiment 11: Power BI Sales Calculations and DAX Measures

dax_measures = """
=== 1. Calculated Columns ===
Total Cost = Sales[Quantity] * Sales[UnitCost]
Profit = Sales[Sales] - Sales[Total Cost]

=== 2. DAX Measures ===
Total Sales = SUM(Sales[Sales])
Total Profit = SUM(Sales[Profit])
Profit Margin % = DIVIDE([Total Profit], [Total Sales]) * 100
Sales % of Total = DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Sales))) * 100
"""

print(dax_measures)
