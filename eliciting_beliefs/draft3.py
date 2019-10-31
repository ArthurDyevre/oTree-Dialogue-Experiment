import numpy as np
import numpy


a1 = np.random.binomial(3, 0.5, 2)
a2 = np.random.binomial(3, 0.5, 2)
a3 = np.random.binomial(3, 0.5, 2)

rt1,rt2= a1 + a2 + a3
print(rt1,rt2)
print(a1)
print(a2)
print(a3)

print("====================")
rt = []
for i in range(10):
    rt =np.random.binomial(3, 0.5, 10) + np.random.binomial(3, 0.5,10) + np.random.binomial(3, 0.5, 10)
print(rt)

print(type(rt[1]))

number_of_students = 30
number_of_rounds = 100
matrix = [[0 for x in range(number_of_rounds)] for y in range(number_of_students)]

print(matrix)

print("============================")

m1 = [1,2,3]
m2 = [1,2,3]

print(np.add(m1,m2))