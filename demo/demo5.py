empty_array = [[None]] * 5

print (empty_array)

#empty_array[0].append(1)
temps = empty_array[0]

for temp in temps:
    temp.append(1)

empty_array[0] = temp


print(empty_array)

#print(empty_array)