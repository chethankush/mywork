# This program checks if a given number is divisible by 5 or 7.
r1 = int(input("Enter the range start value: " ))
r2 = int(input("Enter the range end value: " ))
print(f"Numbers divisible by 7 between {r1} and {r2} are:")
count = 0
r3 = 5
if r1 > r2:
    r3 = -5
for num in range(r1, r2, r3):
    if num % 7 == 0:
        print(num, end=' ')
        print("{num} is divisible by 7 ")
        count += 1

print(f"\nTotal numbers divisible by 7 between {r1} and {r2} are: {count}")