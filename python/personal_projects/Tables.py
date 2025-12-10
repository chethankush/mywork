## Multiplication Table
def calling(num):
    len = 10
    for n in range(1,len+1):
        print(num,"X", n, "=", num*n)

if __name__ == "__main__":
    num = int(input("Enter a number to print its multiplication table: "))
    calling(num)
