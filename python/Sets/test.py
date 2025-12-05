num1 = {1,2,4,4,5,6,7,8,9,1,2}
num2 = {4,10,11,12}

print("disjoint check-->",num1.isdisjoint(num2)) # Disjoint check
if not num1.isdisjoint(num2):
    print("Sets have common numbers")
else:
    print("Sets have no common numbers")