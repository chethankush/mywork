# Prompt the user to input a year and convert it to an integer, assigning it to the variable 'year'
year = int(input("Input a year: "))

# Determine if the input year is a leap year

# Check if the year is divisible by 400
if (year % 400 == 0):
    leap_year = True
# Check if the year is divisible by 100
elif (year % 100 == 0):
    leap_year = False
# Check if the year is divisible by 4
elif (year % 4 == 0):
    leap_year = True
else:
    leap_year = False

# Prompt the user to input a month in the range of 1-12 and convert it to an integer, assigning it to the variable 'month'
month = int(input("Input a month [1-12]: "))

# Determine the number of days in the specified month

# Check for months with 31 days
if month in (1, 3, 5, 7, 8, 10, 12):
    month_length = 31
# Check for February
elif month == 2:
    # Check for leap year and assign the appropriate number of days
    if leap_year:
        month_length = 29
    else:
        month_length = 28
# For months with 30 days
else:
    month_length = 30

# Prompt the user to input a day in the range of 1-31 and convert it to an integer, assigning it to the variable 'day'
day = int(input("Input a day [1-31]: "))

# Calculate the next date based on the provided day, month, and year

# Check if the day is less than the total number of days in the month
if day < month_length:
    day += 1
else:
    day = 1
    # Check if the current month is December
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1

# Display the next date in the format [yyyy-mm-dd] based on the updated day, month, and year
print("The next date is [yyyy-mm-dd] %d-%d-%d." % (year, month, day))
