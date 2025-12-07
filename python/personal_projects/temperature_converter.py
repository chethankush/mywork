#To write a python program that converts temperatures between Celsius and  Fahrenheit.
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32 

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

for i in range(2):
    print("Temperature Converter")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    choice = input("Select an option (1 or 2): ")

    if choice == '1':
        celsius = float(input("Enter temperature in Celsius: "))
        fahrenheit = celsius_to_fahrenheit(celsius)
        print(f"{celsius}°C is equal to {fahrenheit} F")

    elif choice == '2':
        fahrenheit = float(input("Enter temperature in Fahrenheit: "))
        celsius = fahrenheit_to_celsius(fahrenheit)
        print(f"{fahrenheit} F is equal to {celsius}°C")

    else:
        print("Invalid choice. Please select 1 or 2.")