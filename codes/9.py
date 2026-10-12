# ==============================================================================
# LAB CYCLE - 9
# Aim: Write a Python program to implement a Scatter Plot using sample data.
# ==============================================================================

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)
x = np.random.normal(loc=50, scale=10, size=100)
y = np.random.normal(loc=60, scale=15, size=100)

plt.figure(figsize=(6, 4))
plt.scatter(x, y, color='blue', alpha=0.7, edgecolor='black')
plt.title('Scatter Plot of Sample Data')
plt.xlabel('X Values')
plt.ylabel('Y Values')
plt.tight_layout()
plt.show()
