# Experiment 5: Single and Multiple Variable Histograms
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)
dataset1 = np.random.normal(loc=50, scale=10, size=500)
dataset2 = np.random.normal(loc=65, scale=12, size=500)

# 1. Single Variable Histogram
plt.figure(figsize=(6, 4))
plt.hist(dataset1, bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Single Variable Histogram')
plt.tight_layout()
plt.show()

# 2. Multiple Variable Histogram
plt.figure(figsize=(6, 4))
plt.hist(dataset1, bins=20, alpha=0.6, label='Dataset 1', color='skyblue', edgecolor='black')
plt.hist(dataset2, bins=20, alpha=0.6, label='Dataset 2', color='orange', edgecolor='black')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Multiple Variable Histogram')
plt.legend()
plt.tight_layout()
plt.show()
