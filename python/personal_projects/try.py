year = int(input("Enter a year (1,9999): "))
month = int(input("Enter a month (1-12): "))
day = int(input("Enter a day (1-31): "))

if year in range(1, 10000):
    if month in range(1, 13):
        if day in range(1, 32):
            day = day + 1
            print(f"The date is: {day:02d}/{month:02d}/{year}")
        else:
            print("Day is out of range")
    else:
        print("Month is out of range") 
else:
    print("year is out of range")