# ============================================================================
# Experiment 4: Grouped and Stacked Bar Charts
# Libraries: matplotlib, numpy
# ============================================================================

import matplotlib.pyplot as plt
import numpy as np

# Sample Data
regions = ['North', 'South', 'East', 'West']
product1 = [200, 220, 250, 190]
product2 = [150, 180, 200, 160]
product3 = [100, 130, 150, 120]
positions = np.arange(len(regions))
width = 0.25

# ----------------------------------------------------------------------------
# 1. Grouped Bar Chart
# ----------------------------------------------------------------------------
plt.figure(figsize=(6, 4))
plt.bar(positions - width, product1, width, label='Product 1', color='black')
plt.bar(positions,         product2, width, label='Product 2', color='orange')
plt.bar(positions + width, product3, width, label='Product 3', color='green')
plt.xticks(positions, regions)
plt.xlabel('Region')
plt.ylabel('Sales')
plt.title('Grouped Bar Chart of Sales by Region')
plt.legend()
plt.tight_layout()
plt.show()

# ----------------------------------------------------------------------------
# 2. Stacked Bar Chart
# ----------------------------------------------------------------------------
p1 = np.array(product1)
p2 = np.array(product2)
p3 = np.array(product3)

plt.figure(figsize=(6, 4))
plt.bar(positions, p1, label='Product 1', color='black')
plt.bar(positions, p2, bottom=p1, label='Product 2', color='orange')
plt.bar(positions, p3, bottom=p1 + p2, label='Product 3', color='green')
plt.xticks(positions, regions)
plt.xlabel('Region')
plt.ylabel('Sales')
plt.title('Stacked Bar Chart of Sales by Region')
plt.legend()
plt.tight_layout()
plt.show()
