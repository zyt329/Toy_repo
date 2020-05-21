import random
from matplotlib import pyplot as plt
import numpy as np

# Below is our spaghetti code for 3-states CA
rule_number = 76
length = 100
time = 100

# make the initial condition
initial_condition = []
for i in range(length):
    initial_condition.append(random.randint(0, 1))

# create list of neighborhood tuples in lex. order
neighborhoods = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),
                 (1, 2), (2, 0), (2, 1), (2, 2)]

# convert the rule number to binary and padd with 0s as needed
in_ternary = np.base_repr(rule_number, 3)[::-1]
ternary_length = len(in_ternary)
if ternary_length != 9:
    padding = 9 - ternary_length
    in_ternary = in_ternary + '0'*padding

# create the lookup table dictionary
lookup_table = {}
for i in range(9):
    key = neighborhoods[i]
    val = in_ternary[i]
    lookup_table.update({key: val})

# initialize spacetime field and current configuration
spacetime_field = [initial_condition]
current_configuration = initial_condition.copy()

# apply the lookup table to evolve the CA for the given number of time steps
for t in range(time):
    new_configuration = []
    for i in range(len(current_configuration)):

        neighborhood = (current_configuration[(i-1)],
                        current_configuration[i])

        new_configuration.append(int(lookup_table[neighborhood]))

    current_configuration = new_configuration
    spacetime_field.append(new_configuration)

# plot the spacetime field diagram
plt.figure(figsize=(12, 12))
plt.imshow(spacetime_field, cmap=plt.cm.Greys, interpolation='nearest')
plt.show()
