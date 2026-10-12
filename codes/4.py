# ==============================================================================
# LAB CYCLE - 4
# Aim: Write a Python program to Implement or create grouped and stacked bar charts.
# ==============================================================================

# Grouped Bar Chart
import matplotlib.pyplot as plt
import numpy as np

regions = ['North', 'South', 'East', 'West']
product1 = [200, 220, 250, 190]
product2 = [150, 180, 200, 160]
product3 = [100, 130, 150, 120]

positions = np.arange(len(regions))
width = 0.25

plt.figure(figsize=(6, 4))
plt.bar(positions - width, product1, width, label='Product 1', color='black')
plt.bar(positions, product2, width, label='Product 2', color='orange')
plt.bar(positions + width, product3, width, label='Product 3', color='green')
plt.xticks(positions, regions)
plt.xlabel('Region')
plt.ylabel('Sales')
plt.title('Grouped Bar Chart of Sales by Region')
plt.legend()
plt.show()

# Stacked Bar Chart
import matplotlib.pyplot as plt
import numpy as np

regions = ['North', 'South', 'East', 'West']
product1 = np.array([200, 220, 250, 190])
product2 = np.array([150, 180, 200, 160])
product3 = np.array([100, 130, 150, 120])

positions = np.arange(len(regions))
plt.figure(figsize=(6, 4))
plt.bar(positions, product1, label='Product 1', color='black')
plt.bar(positions, product2, bottom=product1, label='Product 2', color='orange')
plt.bar(positions, product3, bottom=product1 + product2, label='Product 3', color='green')
plt.xticks(positions, regions)
plt.xlabel('Region')
plt.ylabel('Sales')
plt.title('Stacked Bar Chart of Sales by Region')
plt.legend()
plt.show()
