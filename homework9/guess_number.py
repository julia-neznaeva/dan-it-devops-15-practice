import random

print("Lets play. You have 5 attempts to guess the number between 1 and 100:.")
number = random.randint(1, 100)
for i in range(5):

    guess = int(input(f"Attempt {i+1}: Enter your guess: ".format(i + 1)))
    if guess < number:
        print("Too low!")
    elif guess > number:
        print("Too high!")
    else:
        print("Congratulations! You guessed the number.")
        break

print("Game over!")
print("The number was:", number)
