from collections import defaultdict

def get_elements_with_same_values(dictionary):
    grouped_elements = defaultdict(list)
    for key, value in dictionary.items():
        grouped_elements[value].append(key)
    return grouped_elements

# Example dictionary
my_dict = {'a': 1, 'b': 2, 'c': 1, 'd': 2, 'e': 3}

# Get elements with same values
results = get_elements_with_same_values(my_dict)

# Print keys and values separately
for value, keys in results.items():
    print("Keys:", keys)
    #print("Keys with value", value, ":", keys)
    print("Values:", value)