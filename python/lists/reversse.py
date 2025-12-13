#To reverse a list in Python, you can use the built-in reverse() method or slicing. Here are examples of both methods:
# Using the reverse() method
my_list = [1, 2, 3, 4, 5]
print("Original list:", my_list)
my_list.reverse()
print("Reversed list using reverse():", my_list)
# Using slicing
my_list = [1, 2, 3, 4, 5]
reversed_list = my_list[::-1]
print("Reversed list using slicing:", reversed_list)
# Output:
# Reversed list using reverse(): [5, 4, 3, 2, 1]
# Reversed list using slicing: [5, 4, 3, 2, 1]