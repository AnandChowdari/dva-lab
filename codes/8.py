# ==============================================================================
# LAB CYCLE - 8
# Aim: Write a Python program to implement a Q-Q (quantile-quantile) plot to compare two datasets.
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
data1 = np.random.normal(0, 1, 1000)
data2 = np.random.normal(1, 1.5, 1000)

q1 = np.sort(data1)
q2 = np.sort(data2)

plt.figure(figsize=(6, 4))
plt.scatter(q1, q2, s=10, color='blue')
lims = [min(q1.min(), q2.min()), max(q1.max(), q2.max())]
plt.plot(lims, lims, 'r--', label='y = x (same distribution)')
plt.xlabel('Quantiles of Dataset 1')
plt.ylabel('Quantiles of Dataset 2')
plt.title('Q-Q Plot to Compare Two Datasets')
plt.legend()
plt.show()
