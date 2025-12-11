# To print a diamond pattern using asterisks.
def print_diamond(n):
    # Print the upper part of the diamond
    for i in range(n):
        print(' ' * (n - i - 1) + '*' * (2 * i + 1))
    
    # Print the lower part of the diamond
    for i in range(n - 2, -1, -1):
        print(' ' * (n - i - 1) + '*' * (2 * i + 1))

if __name__ == "__main__":
    n = int(input("Enter the number of rows for the diamond pattern: "))
    print_diamond(n)

##################################################

def try_function():
    num = int(input("Enter a number: "))

    #Upper part of diamond
    for i in range(num):
        print( "*" * (i + 1))

    #Lower part of diamond
    for i in range(num - 1, 0, -1):
        print( "*" * i)

if __name__ == "__main__":
    try_function()