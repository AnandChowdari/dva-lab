# ============================================================================
# Experiment 7: Empirical Cumulative Distribution Function (ECDF) Plot
# Libraries: matplotlib, numpy, statsmodels
# ============================================================================

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Generate Reproducible Sample Data
np.random.seed(0)
data = np.random.normal(0, 1, 100)

# Compute ECDF Using Statsmodels
ecdf = sm.distributions.ECDF(data)
x = np.linspace(min(data), max(data), num=200)
y = ecdf(x)

# Plot ECDF as Step Function
plt.figure(figsize=(6, 4))
plt.step(x, y, color='steelblue', where='post', linewidth=1.5)
plt.xlabel('X-axis Label')
plt.ylabel('ECDF')
plt.title('Empirical Cumulative Distribution Function (ECDF)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
