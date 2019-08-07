
import numpy as np

l = []
for i in range(10):
    x = np.random.negative_binomial(3, 0.5, 10) + np.random.negative_binomial(3, 0.5, 10) + np.random.negative_binomial(3, 0.5, 10)
    l.append(x)

m = []
for i in l:
    m.append(max(i))

print(max(m))