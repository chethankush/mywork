# Write a python program to check whether the numbers in a list are even or odd.
def try_even_odd(num):
    print("Original List:", num)
    length = len(num)
    for i in range(length -1):
        if num[i] % 2 == 0:
            print(f"{num[i]} is even")
        else:
            print(f"{num[i]} is odd")

if __name__ == "__main__":
    num = [10, 21, 4, 45, 66, 93, 11]
    try_even_odd(num)

######################################################
def even_odd():
    num = int(input("Enter a number: "))
    if num % 2 == 0:
        print(f"{num} is even")
    else:
        print(f"{num} is odd")

if __name__ == "__main__":
    even_odd()