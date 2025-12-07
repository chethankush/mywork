#To guess a number between 1 and 100.
import random
def number_guessing_game():
    r1 = 100
    number_to_guess = random.randint(1, r1)
    attempts = 0
    print("Welcome to the Number Guessing Game!")
    print(f"I have selected a number between 1 and {r1}. Can you guess it?")

    while True:
        try:
            user_guess = int(input("Enter your guess: "))
            attempts += 1

            if user_guess < 1 or user_guess > r1:
                print(f"Please guess a number within the range of 1 to {r1}.")
                continue

            if user_guess < number_to_guess:
                print("Too low! Try again.")
            elif user_guess > number_to_guess:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You've guessed the number {number_to_guess} in {attempts} attempts.")
                break
        except ValueError:
            print(f"Invalid input. Please enter an integer between 1 and {r1}.")

if __name__ == "__main__":
    number_guessing_game()