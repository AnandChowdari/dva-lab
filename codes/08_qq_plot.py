# ============================================================================
# Experiment 8: Q-Q Plot to Compare Two Datasets
# Libraries: matplotlib, numpy, scipy
# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Generate Two Normal Datasets with Different Means and Variances
np.random.seed(0)
data1 = np.random.normal(0, 1, 1000)      # Mean=0, Std=1
data2 = np.random.normal(1, 1.5, 1000)    # Mean=1, Std=1.5

# Render Q-Q Plot Against Theoretical Normal Quantiles
plt.figure(figsize=(6, 4))
stats.probplot(data1, dist="norm", plot=plt)
stats.probplot(data2, dist="norm", plot=plt)
plt.title('Q-Q Plot to Compare Two Datasets')
plt.xlabel('Theoretical Quantiles')
plt.ylabel('Sample Quantiles')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
