# A simple Python program to print a pattern based on user input
def calling(num):
    for n in range(1,num+1):
        for i in range(0,n):
            print(n,end="")
        print("")

if __name__ == "__main__":
    num = int(input("Enter a number: "))
    calling(num)

    #################################Better Approach#################################
def calling(num):
    for n in range(1,num+1):
        print(str(n) * n)

if __name__ == "__main__":
    num = int(input("Enter a number: "))
    calling(num)