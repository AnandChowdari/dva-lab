# Experiment 9: Scatter Plot Using Sample Data
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)
x = np.random.rand(50) * 10
y = 2.5 * x + np.random.randn(50) * 2

plt.figure(figsize=(6, 4))
plt.scatter(x, y, color='teal', alpha=0.7, edgecolors='black')
plt.xlabel('X (Sample Feature)')
plt.ylabel('Y (Target)')
plt.title('Scatter Plot of Sample Data')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
