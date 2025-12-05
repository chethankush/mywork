numbers = [1,2,3,4,5,1,2,3]
first =set(numbers)
second = {4,5}
print("Uniom of two sets-->",first | second) # Union of two sets
print("Intersection of two sets-->",first & second) # Intersection of two sets
print("Difference of two sets-->",first - second) # Difference of two sets
print("Symmetric difference of two sets-->",first ^ second) # Symmetric difference of two sets
print("Subset check-->",first <= second) # Subset check
print("Superset check-->",first >= second) # Superset check
print("Disjoint check-->",first.isdisjoint(second)) # Disjoint check
print("Adding an element to a set-->",first.add(6)) # Adding an element to a set
print("Removing an element from a set-->",first.remove(1)) # Removing an element from a set

print("first set --> ",first)
print("second set -->",second)
print("first set clearing -->",first.clear()) # Clearing a set
print("after  clearing-->",first)
