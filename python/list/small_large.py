# Find Largest and Smallest Number in a List
def calling(num):
    num = sorted(num)
    print("Sorted List:", num)
    len_num = len(num)
    print(" The largest number in the list is:", num[len_num - 1])
    print(" The smallest number in the list is:", num[0])

num = []
while True:
    n = int(input("Enter a number (0 to stop): "))
    if n == 0:
        break
    num.append(n)
print("Original List:", num)
calling(num)