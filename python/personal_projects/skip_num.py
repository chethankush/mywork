# This function iterates through numbers 0 to 10 and skips printing the numbers 3 and 6.
def calling():
    num = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
    for n in num:
        if n == 3  or n == 6:
            continue
        print("Current number:", n)

if __name__ == "__main__":
    calling()