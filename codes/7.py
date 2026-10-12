# Experiment 7: Empirical Cumulative Distribution Function (ECDF) Plot
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

np.random.seed(0)
data = np.random.normal(loc=0, scale=1, size=100)

# Compute ECDF
ecdf = sm.distributions.ECDF(data)
x = np.linspace(min(data), max(data), 100)
y = ecdf(x)

plt.figure(figsize=(6, 4))
plt.step(x, y, where='post', label='ECDF', color='purple')
plt.xlabel('Value')
plt.ylabel('P(X <= x)')
plt.title('Empirical Cumulative Distribution Function (ECDF)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
