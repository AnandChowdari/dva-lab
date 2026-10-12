# ==============================================================================
# LAB CYCLE - 10
# Aim: Using Power BI, perform sales data visualization using predefined fields.
# ==============================================================================

"""
Dataset used (sales_data.csv). Sales = Quantity * UnitPrice.

OrderID,OrderDate,Region,Category,Product,Quantity,UnitPrice,UnitCost,Sales
1,2024-01-05,East,Electronics,Laptop,5,800,600,4000
2,2024-01-12,West,Electronics,Phone,10,400,300,4000
3,2024-02-03,North,Furniture,Chair,20,100,70,2000
4,2024-02-15,South,Furniture,Desk,4,300,200,1200
5,2024-03-07,East,Electronics,Tablet,12,350,250,4200
6,2024-03-21,West,Furniture,Chair,15,100,70,1500
7,2024-04-02,North,Electronics,Laptop,3,800,600,2400
8,2024-04-18,South,Electronics,Phone,8,400,300,3200
9,2024-05-09,East,Furniture,Desk,6,300,200,1800
10,2024-05-25,West,Electronics,Laptop,7,800,600,5600

Procedure:
1. Open Power BI Desktop and click Home -> Get data -> Text/CSV.
2. Select sales_data.csv and click Load.
3. Check in the Data pane that the table Sales and all its fields are loaded.
4. Clustered column chart: select the visual, drag Region to X-axis and Sales to Y-axis (Sum of Sales).
5. Pie chart: drag Category to Legend and Sales to Values.
6. Line chart: drag OrderDate to X-axis (keep only Month) and Sales to Y-axis.
7. Card: drag Sales to Fields to display the total sales (29,900).
8. Slicer: drag Region to a Slicer visual to filter all the charts.

Output Values Shown by Visuals:
- Region Sum of Sales: East (10,000), North (4,400), South (4,400), West (11,100) -> Total: 29,900
- Category Sum of Sales: Electronics (23,400), Furniture (6,500)
- Month Sum of Sales: January (8,000), February (3,200), March (5,700), April (5,600), May (7,400)
"""

import pandas as pd
import io

sales_csv = """OrderID,OrderDate,Region,Category,Product,Quantity,UnitPrice,UnitCost,Sales
1,2024-01-05,East,Electronics,Laptop,5,800,600,4000
2,2024-01-12,West,Electronics,Phone,10,400,300,4000
3,2024-02-03,North,Furniture,Chair,20,100,70,2000
4,2024-02-15,South,Furniture,Desk,4,300,200,1200
5,2024-03-07,East,Electronics,Tablet,12,350,250,4200
6,2024-03-21,West,Furniture,Chair,15,100,70,1500
7,2024-04-02,North,Electronics,Laptop,3,800,600,2400
8,2024-04-18,South,Electronics,Phone,8,400,300,3200
9,2024-05-09,East,Furniture,Desk,6,300,200,1800
10,2024-05-25,West,Electronics,Laptop,7,800,600,5600"""

df = pd.read_csv(io.StringIO(sales_csv))
print("=== sales_data.csv ===")
print(df)
