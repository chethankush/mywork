def even_odd():
    num = int(input("Enter a number: "))
    if num % 2 == 0:
        print(f"{num} is even")
    else:
        print(f"{num} is odd")

if __name__ == "__main__":
    even_odd()