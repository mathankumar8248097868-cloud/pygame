import random

words = ["python", "programming", "computer", "algorithm"]
word = random.choice(words)
word_letters = set(word)
guessed_letters = set()
attempts = 6

while attempts > 0 and word_letters != guessed_letters:
    print(f"\nAttempts left: {attempts}")
    print("Word: ", end="")
    for letter in word:
        if letter in guessed_letters:
            print(letter, end=" ")
        else:
            print("_", end=" ")
    guess = input("\nGuess a letter: ").lower()
    if guess in guessed_letters:
        print("You already guessed that!")
    elif guess in word_letters:
        guessed_letters.add(guess)
    else:
        attempts -= 1
        print("Wrong guess!")
    if word_letters == guessed_letters:
        print(f"\nCongratulations! You guessed '{word}'!")
        break
if attempts == 0:
    print(f"\nGame Over! The word was '{word}'.")
