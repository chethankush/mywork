#To write program to find the median of given numbers using conditional loops
def find_median(numbers):
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)

    print("Sorted numbers:", sorted_numbers)
    
    if n % 2 == 1:
        median = sorted_numbers[n // 2]
    else:
        median = (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2
    
    return median

# Example usage
numbers = [12, 3, 5, 7, 19,6]
median = find_median(numbers)
print("The median is:", median)