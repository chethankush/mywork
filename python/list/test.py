# To check if list is empty or not
def is_list_empty(lst):
    if not lst:
        print("List is empty")
    else:
        print("List is not empty")
    return None        
# Test cases
num = []
print(is_list_empty(num))          # Expected output: True
num = [1, 2, 3]
print(is_list_empty(num))          # Expected output: False
strs = []
strs = num 
print("strs is :",strs)