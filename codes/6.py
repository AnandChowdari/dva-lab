# ==============================================================================
# LAB CYCLE - 6
# Aim: Write a Python program to implement density plot using single and multiple variable distribution.
# ==============================================================================

# Density Plot - Single Variable
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

np.random.seed(0)
scores = np.random.normal(loc=75, scale=10, size=100)

plt.figure(figsize=(6, 4))
sns.kdeplot(scores, color='steelblue', fill=True)
plt.title('Density Plot of Test Scores (Single Variable)')
plt.xlabel('Test Scores')
plt.ylabel('Density')
plt.tight_layout()
plt.show()

# Density Plot - Multiple Variables
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

np.random.seed(0)
maths = np.random.normal(loc=75, scale=10, size=100)
science = np.random.normal(loc=65, scale=12, size=100)

plt.figure(figsize=(6, 4))
sns.kdeplot(maths, color='steelblue', fill=True, label='Maths')
sns.kdeplot(science, color='orange', fill=True, label='Science')
plt.title('Density Plot of Test Scores (Multiple Variables)')
plt.xlabel('Test Scores')
plt.ylabel('Density')
plt.legend()
plt.tight_layout()
plt.show()
