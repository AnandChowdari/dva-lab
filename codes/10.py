# Experiment 10: Power BI Sales Data Visualization
import pandas as pd
import io

csv_data = """OrderID,OrderDate,Region,Category,Product,Quantity,UnitPrice,UnitCost,Sales
101,2024-01-05,North,Electronics,Laptop,2,1000,700,2000
102,2024-01-06,South,Electronics,Phone,5,500,300,2500
103,2024-01-10,North,Furniture,Chair,10,150,100,1500
104,2024-01-12,East,Furniture,Table,3,400,250,1200
105,2024-01-15,West,Electronics,Tablet,4,600,400,2400
106,2024-01-18,West,Electronics,Phone,6,500,300,3000
107,2024-01-20,East,Electronics,Laptop,3,1000,700,3000
108,2024-01-22,South,Furniture,Chair,8,150,100,1200
109,2024-01-25,North,Electronics,Tablet,5,600,400,3000
110,2024-01-28,South,Electronics,Laptop,10,1000,700,10000"""

df = pd.read_csv(io.StringIO(csv_data))
print("Sample Dataset:")
print(df)

print("\n--- Power BI Visuals Setup ---")
print("1. Clustered Column Chart: X=Region, Y=Sum of Sales")
print("2. Pie Chart: Legend=Category, Values=Sum of Sales")
print("3. Line Chart: X=OrderDate, Y=Sum of Sales")
print("4. KPI Card: Fields=Sum of Sales (Total: 29,900)")
print("5. Slicers: Filter by Region and Category")
