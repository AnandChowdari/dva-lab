# ==============================================================================
# LAB CYCLE - 5
# Aim: Write a Python program to implement histogram using single and multiple variable distribution.
# ==============================================================================

# Histogram - Single Variable
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)
scores = np.random.normal(loc=75, scale=10, size=100)

plt.figure(figsize=(6, 4))
plt.hist(scores, bins=8, color='steelblue', edgecolor='black')
plt.title('Histogram of Test Scores (Single Variable)')
plt.xlabel('Test Scores')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Histogram - Multiple Variables
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)
maths = np.random.normal(loc=75, scale=10, size=100)
science = np.random.normal(loc=65, scale=12, size=100)

plt.figure(figsize=(6, 4))
plt.hist(maths, bins=8, alpha=0.6, color='steelblue', edgecolor='black', label='Maths')
plt.hist(science, bins=8, alpha=0.6, color='orange', edgecolor='black', label='Science')
plt.title('Histogram of Test Scores (Multiple Variables)')
plt.xlabel('Test Scores')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.show()
