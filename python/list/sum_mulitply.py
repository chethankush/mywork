# Sum and Product of List elements
def calling(num):
    sum = 0
    for i in num:
        sum += i
    print("Sum of List elements:", sum)
    total = 1
    for i in num:
        total = total * i
    print("Product of List elements:", total)

num = []
while True:
    n = int(input("Enter a number (0 to stop): "))
    if n == 0:
        break
    num.append(n)
print("Original List:", num)
calling(num)
