#!/usr/bin/env python3
import math

def show_menu():
    print("\n================ STANDARD CALCULATOR ================")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Modulus")
    print("6. Power")
    print("7. Square Root")
    print("8. Exit")
    print("====================================================")

def get_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def calculator():
    while True:
        show_menu()
        choice = input("Select an option (1-8): ")

        if choice == "1":
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")
            print(f"Result = {a + b}")

        elif choice == "2":
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")
            print(f"Result = {a - b}")

        elif choice == "3":
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")
            print(f"Result = {a * b}")

        elif choice == "4":
            a = get_number("Enter numerator: ")
            b = get_number("Enter denominator: ")
            if b == 0:
                print("Error: Division by zero is not allowed.")
            else:
                print(f"Result = {a / b}")

        elif choice == "5":
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")
            print(f"Result = {a % b}")

        elif choice == "6":
            a = get_number("Enter base: ")
            b = get_number("Enter exponent: ")
            print(f"Result = {a ** b}")

        elif choice == "7":
            a = get_number("Enter number: ")
            if a < 0:
                print("Error: Cannot compute square root of a negative number.")
            else:
                print(f"Result = {math.sqrt(a)}")

        elif choice == "8":
            print("Exiting Calculator... Goodbye!")
            break

        else:
            print("Invalid choice. Select between 1 and 8.")

# Entry point
if __name__ == "__main__":
    calculator()
