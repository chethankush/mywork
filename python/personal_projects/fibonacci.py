# write a python program to print fibonacci series up to n terms
def calling(num):
    flag = True
    temp1 = 0
    temp2 = 1

    for n in range(num-1):
        if flag: 
            print(temp1)
            print(temp2)
            flag = False
            final = temp1 + temp2
        else:
            print(final," ")
            temp1 = temp2
            temp2 = final
            final = temp1 + temp2
def sayit():
    num = int(input("Enter the number of terms you want in Fibonacci series: "))
    calling(num)
if __name__ == "__main__":
    sayit()
