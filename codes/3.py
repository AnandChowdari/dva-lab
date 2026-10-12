# Experiment 3: Vertical and Horizontal Bar Charts
import matplotlib.pyplot as plt
import numpy as np

# Sample Data
regions = ['North', 'South', 'East', 'West']
sales = [200, 220, 250, 190]
positions = np.arange(len(regions))

# 1. Vertical Bar Chart
plt.figure(figsize=(6, 4))
plt.bar(positions, sales, color='steelblue')
plt.xticks(positions, regions)
plt.xlabel('Region')
plt.ylabel('Sales')
plt.title('Vertical Bar Chart of Sales by Region')
plt.tight_layout()
plt.show()

# 2. Horizontal Bar Chart
plt.figure(figsize=(6, 4))
plt.barh(positions, sales, color='steelblue')
plt.yticks(positions, regions)
plt.xlabel('Sales')
plt.ylabel('Region')
plt.title('Horizontal Bar Chart of Sales by Region')
plt.tight_layout()
plt.show()
