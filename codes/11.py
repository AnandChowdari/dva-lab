# ==============================================================================
# LAB CYCLE - 11
# Aim: Using Power BI, perform sales calculation and percentage analysis using calculated columns and DAX measures.
# ==============================================================================

"""
Procedure:
1. Open Power BI Desktop and click Home -> Get data -> Text/CSV.
2. Select sales_data.csv and click Load.
3. Use the same sales_data.csv table (Sales) as in Experiment 10.

Calculated columns (Modeling -> New column):
Total Cost = Sales[Quantity] * Sales[UnitCost]
Profit = Sales[Sales] - Sales[Total Cost]

Measures (Modeling -> New measure):
Total Sales = SUM(Sales[Sales])
Total Profit = SUM(Sales[Profit])
Profit Margin % = DIVIDE([Total Profit], [Total Sales]) * 100
Sales % of Total = DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Sales))) * 100

Visuals Setup:
1. Insert a Table visual and drag Region, Total Sales, Total Profit, Profit Margin % and Sales % of Total into it.
2. Insert a Card for Total Sales (29,900) and another Card for Total Profit (8,050).
3. Insert a Clustered bar chart with Region on the axis and Sales % of Total as the value.

Output Summary:
Region   Total Sales  Total Profit  Profit Margin %  Sales % of Total
East     10,000       2,800         28.00            33.44
North    4,400        1,200         27.27            14.72
South    4,400        1,200         27.27            14.72
West     11,100       2,850         25.68            37.12
Total    29,900       8,050         26.92            100.00
"""

# DAX Formulas:
calculated_columns = '''
Total Cost = Sales[Quantity] * Sales[UnitCost]
Profit = Sales[Sales] - Sales[Total Cost]
'''

dax_measures = '''
Total Sales = SUM(Sales[Sales])
Total Profit = SUM(Sales[Profit])
Profit Margin % = DIVIDE([Total Profit], [Total Sales]) * 100
Sales % of Total = DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Sales))) * 100
'''

print("=== CALCULATED COLUMNS (Modeling -> New column) ===")
print(calculated_columns.strip())
print("\n=== DAX MEASURES (Modeling -> New measure) ===")
print(dax_measures.strip())
