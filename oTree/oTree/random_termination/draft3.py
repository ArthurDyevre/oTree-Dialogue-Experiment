import numpy as np
import numpy
from otree.models import group, player
from . import pages, models,tests

round_test =[]

a1 = np.random.binomial(3, 0.5, 2)
a2 = np.random.binomial(3, 0.5, 2)
a3 = np.random.binomial(3, 0.5, 2)

rt1,rt2= a1 + a2 + a3
print(rt1,rt2)
print(a1)
print(a2)
print(a3)

print("====================")
number_of_students = 30
number_of_rounds = 100
matrix = [[0 for x in range(number_of_rounds)] for y in range(number_of_students)]



# rt = np.random.negative_binomial(3, 0.5, 100000000) + np.random.negative_binomial(3, 0.5, 100000000) + np.random.negative_binomial(3, 0.5, 100000000)
# print(rt)
# unique_elements, counts_elements = np.unique(rt, return_counts=True)
# print("Frequency of unique values of the said array:")
# print(np.asarray((unique_elements, counts_elements)))

print(round_test)