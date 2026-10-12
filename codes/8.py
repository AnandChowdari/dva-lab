# Experiment 8: Q-Q Plot to Compare Two Datasets
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

np.random.seed(0)
sample_data = np.random.normal(loc=0, scale=1, size=100)

plt.figure(figsize=(6, 4))
stats.probplot(sample_data, dist="norm", plot=plt)
plt.title('Q-Q Plot against Normal Distribution')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
