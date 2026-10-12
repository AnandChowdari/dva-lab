# ==============================================================================
# LAB CYCLE - 7
# Aim: Write a Python program to implement an Empirical Cumulative Distribution Function (ECDF) plot.
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
data = np.random.normal(0, 1, 100)

x = np.sort(data)
y = np.arange(1, len(x) + 1) / len(x)

plt.figure(figsize=(6, 4))
plt.step(x, y, where='post')
plt.xlabel('Data Values')
plt.ylabel('ECDF')
plt.title('Empirical Cumulative Distribution Function (ECDF)')
plt.grid(True)
plt.show()
