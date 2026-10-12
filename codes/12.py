# ==============================================================================
# LAB CYCLE - 12
# Aim: Using Power BI, perform conditional and logical analysis using IF, AND, OR, and display totals and percentages using visualizations.
# ==============================================================================

"""
Procedure:
1. Open Power BI Desktop and click Home -> Get data -> Text/CSV.
2. Select sales_data.csv and click Load.
3. Use the same sales_data.csv table (Sales) as in Experiment 10, with the Profit column from Experiment 11.

Calculated columns using IF, AND, OR (Modeling -> New column):
Sales Level =
IF(Sales[Sales] >= 5000, "High",
   IF(Sales[Sales] >= 2500, "Medium", "Low"))

Bulk East Order = IF(AND(Sales[Quantity] >= 10, Sales[Region] = "East"), "Yes", "No")

Focus Order = IF(OR(Sales[Region] = "West", Sales[Profit] >= 1000), "Yes", "No")

Measures for totals and percentages (Modeling -> New measure):
Total Sales = SUM(Sales[Sales])
Order Count = COUNTROWS(Sales)
Sales % = DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Sales))) * 100

Visuals Setup:
1. Insert a Table visual with OrderID, Region, Sales, Sales Level, Bulk East Order and Focus Order.
2. Insert a Clustered column chart: Sales Level on X-axis and Order Count on Y-axis.
3. Insert a Pie chart: Focus Order as Legend and Total Sales as Values (show percentage labels).
4. Insert Cards for Total Sales (29,900) and Order Count (10).

Output Summary:
Sales Level  Order Count  Total Sales  Sales %
High         1            5,600        18.73
Medium       4            15,400       51.51
Low          5            8,900        29.77
Total        10           29,900       100.00

Focus Order  Order Count  Total Sales  Sales %
Yes          5            19,300       64.55
No           5            10,600       35.45
"""

# DAX Formulas:
calculated_columns = '''
Sales Level =
IF(Sales[Sales] >= 5000, "High",
   IF(Sales[Sales] >= 2500, "Medium", "Low"))

Bulk East Order = IF(AND(Sales[Quantity] >= 10, Sales[Region] = "East"), "Yes", "No")

Focus Order = IF(OR(Sales[Region] = "West", Sales[Profit] >= 1000), "Yes", "No")
'''

measures = '''
Total Sales = SUM(Sales[Sales])
Order Count = COUNTROWS(Sales)
Sales % = DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Sales))) * 100
'''

print("=== CALCULATED COLUMNS USING IF, AND, OR (Modeling -> New column) ===")
print(calculated_columns.strip())
print("\n=== MEASURES FOR TOTALS & PERCENTAGES (Modeling -> New measure) ===")
print(measures.strip())
