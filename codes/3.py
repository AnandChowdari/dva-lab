# ==============================================================================
# LAB CYCLE - 3
# Aim: Write a Python program to Implement or create horizontal and vertical bar charts.
# ==============================================================================

# Vertical Bar Chart
import matplotlib.pyplot as plt
import numpy as np

regions = ['North', 'South', 'East', 'West']
sales = [200, 220, 250, 190]

positions = np.arange(len(regions))
plt.figure(figsize=(6, 4))
plt.bar(positions, sales, color='steelblue')
plt.xticks(positions, regions)
plt.xlabel('Region')
plt.ylabel('Sales')
plt.title('Vertical Bar Chart of Sales by Region')
plt.show()

# Horizontal Bar Chart
import matplotlib.pyplot as plt
import numpy as np

regions = ['North', 'South', 'East', 'West']
sales = [200, 220, 250, 190]

positions = np.arange(len(regions))
plt.figure(figsize=(6, 4))
plt.barh(positions, sales, color='steelblue')
plt.yticks(positions, regions)
plt.xlabel('Sales')
plt.ylabel('Region')
plt.title('Horizontal Bar Chart of Sales by Region')
plt.show()
