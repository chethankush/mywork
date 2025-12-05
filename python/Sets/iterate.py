
num = {1,2,3,4,5,6,6,7,8,9,1,2}
print("Iterating through set elements:")
for n in num:
    print(n, end=' ')
print("\n",num)  # for newline
print(num.pop())  # This will raise an error because pop() does not take any arguments
print("After popping an element -->",num)
print(len(num)) # Length of the set
print("Initial set -->",num)
num1 = num.add(10)
print("After adding an element -->",num)
num2 = num.remove(4)
print("After removing an element -->",num)

string = {"apple", "banana", "cherry", "apple", "banana"}
print("Iterating through set elements:")
for s in string:
    print(s, end=' ')  
print("\n",string)  # for newline
