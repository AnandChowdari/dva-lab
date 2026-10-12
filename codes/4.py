# Experiment 4: Grouped and Stacked Bar Charts
import matplotlib.pyplot as plt
import numpy as np

# Sample Data
regions = ['North', 'South', 'East', 'West']
q1_sales = [200, 220, 250, 190]
q2_sales = [180, 240, 230, 210]
positions = np.arange(len(regions))
bar_width = 0.35

# 1. Grouped Bar Chart
plt.figure(figsize=(7, 4))
plt.bar(positions - bar_width/2, q1_sales, width=bar_width, label='Q1 Sales', color='steelblue')
plt.bar(positions + bar_width/2, q2_sales, width=bar_width, label='Q2 Sales', color='orange')
plt.xticks(positions, regions)
plt.xlabel('Region')
plt.ylabel('Sales')
plt.title('Grouped Bar Chart of Sales by Region')
plt.legend()
plt.tight_layout()
plt.show()

# 2. Stacked Bar Chart
plt.figure(figsize=(6, 4))
plt.bar(positions, q1_sales, label='Q1 Sales', color='steelblue')
plt.bar(positions, q2_sales, bottom=q1_sales, label='Q2 Sales', color='orange')
plt.xticks(positions, regions)
plt.xlabel('Region')
plt.ylabel('Sales')
plt.title('Stacked Bar Chart of Sales by Region')
plt.legend()
plt.tight_layout()
plt.show()
