# ============================================================================
# Experiment 9: Scatter Plot Using Sample Data
# Libraries: matplotlib, numpy
# ============================================================================

import matplotlib.pyplot as plt
import numpy as np

# Generate Bivariate Sample Data
np.random.seed(0)
x = np.random.normal(loc=50, scale=10, size=100)
y = np.random.normal(loc=60, scale=15, size=100)

# Render Scatter Plot
plt.figure(figsize=(6, 4))
plt.scatter(x, y, color='blue', alpha=0.7, edgecolor='black')
plt.title('Scatter Plot of Sample Data')
plt.xlabel('X Values')
plt.ylabel('Y Values')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
