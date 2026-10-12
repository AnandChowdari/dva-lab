# Experiment 6: Single and Multiple Variable Density Plots
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

np.random.seed(0)
dataset1 = np.random.normal(loc=50, scale=10, size=500)
dataset2 = np.random.normal(loc=65, scale=12, size=500)

# 1. Single Variable Density Plot
plt.figure(figsize=(6, 4))
sns.kdeplot(dataset1, fill=True, color='blue')
plt.xlabel('Value')
plt.ylabel('Density')
plt.title('Single Variable Density Plot')
plt.tight_layout()
plt.show()

# 2. Multiple Variable Density Plot
plt.figure(figsize=(6, 4))
sns.kdeplot(dataset1, fill=True, label='Dataset 1', color='blue')
sns.kdeplot(dataset2, fill=True, label='Dataset 2', color='orange')
plt.xlabel('Value')
plt.ylabel('Density')
plt.title('Multiple Variable Density Plot')
plt.legend()
plt.tight_layout()
plt.show()
