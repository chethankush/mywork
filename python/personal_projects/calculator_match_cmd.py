import math
def show_menu():
    print("====================================================")
    print("Welcome to the Python Calculator!")
    print("Select an operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Exit")
    print("====================================================")

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def calculator():
    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ")
        match choice:

            case 1:
                num1 = get_number("Enter first number: ")
                num2 = get_number("Enter second number: ")
                print(f"The result of {num1} + {num2} = {num1 + num2}")

            case '2':
                num1 = get_number("Enter first number: ")
                num2 = get_number("Enter second number: ")
                print(f"The result of {num1} - {num2} = {num1 - num2}")

            case '3':
                num1 = get_number("Enter first number: ")
                num2 = get_number("Enter second number: ")
                print(f"The result of {num1} * {num2} = {num1 * num2}")

            case '4':
                num1 = get_number("Enter numerator: ")
                num2 = get_number("Enter denominator: ")
                if num2 == 0:
                    print("Error: Division by zero is not allowed.")
                else:
                    print(f"The result of {num1} / {num2} = {num1 / num2}")

            case '5':
                print("Exiting the calculator. Goodbye!")
                break

            case _:
                print("Invalid choice. Please select a valid operation.")

if __name__ == "__main__":
    calculator()