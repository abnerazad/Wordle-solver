import requests
import random
import os

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Introductory function to display rules and instructions
def show_intro():
    clear_console()
    print("Welcome to the Wordle Solver Game!")
    print("------------------------------------")
    print("Rules and Instructions:")
    print("1. The solver will attempt to guess the word you have in mind.")
    print("2. After each guess, provide feedback using:")
    print("   - 'G' for a correct letter in the correct position.")
    print("   - 'Y' for a correct letter in the wrong position.")
    print("   - 'B' for an incorrect letter.")
    print("   - 'R' to retry with a new word.")
    print("   - 'A' to restart the game.")
    print("3. Try to guess the word within the allowed number of attempts!")
    print("Developed by Abner Azad")
    print("\nPress Enter to start the game...")
    input()  # Wait for the user to press Enter
    clear_console()

# Fetch word list from an online source and filter by word length
def fetch_word_list(url, word_length):
    response = requests.get(url)
    response.raise_for_status()  # Check if request was successful
    # Filter words to include only those of the specified length
    return {word.strip().lower() for word in response.text.splitlines() if len(word.strip()) == word_length}

# Improved feedback function to handle repeated letters correctly
def get_feedback(guess, solution):
    feedback = ['B'] * len(guess)  # Start with all 'B'
    solution_letters = list(solution)  # Convert solution to a list to track letters
    
    # First pass: Check for correct positions (Green - 'G')
    for i in range(len(guess)):
        if guess[i] == solution[i]:
            feedback[i] = 'G'
            solution_letters[i] = None  # Mark this letter as used

    # Second pass: Check for correct letters in wrong positions (Yellow - 'Y')
    for i in range(len(guess)):
        if feedback[i] == 'B' and guess[i] in solution_letters:
            feedback[i] = 'Y'
            solution_letters[solution_letters.index(guess[i])] = None  # Mark this letter as used
    
    return ''.join(feedback)

# Function to filter words based on feedback
def filter_words(words, guess, feedback):
    filtered_words = []
    for word in words:
        if get_feedback(guess, word) == feedback:
            filtered_words.append(word)
    return filtered_words

# Main Wordle solver function
def wordle_solver(words, max_attempts=6):
    while True:
        attempts = 0
        possible_words = list(words)  # Convert set to list
        
        while attempts < max_attempts:
            guess = random.choice(possible_words)
            print(f'Attempt {attempts + 1}: {guess}')
            feedback = input('Enter feedback (G, Y, B, R=Retry): ').upper()
            
            if feedback == 'R':
                # Retry with a new word without filtering
                print("Retrying with a new word...")
                continue
            
            if feedback == 'A':
                # Restart the game
                print("Restarting the game...")
                clear_console()  # Clear the console before restarting
                return  # Return to restart the entire process

            if feedback == 'G' * len(guess):  # Check for the correct word length
                print(f'Correct! The word was {guess}')
                input("Press Enter to start a new game...")  # Pause before clearing
                clear_console()  # Clear the console before starting a new game
                break  # Exit the inner loop to start over
            
            possible_words = filter_words(possible_words, guess, feedback)
            if not possible_words:
                print('Ops! No possible words left!')
                break  # Exit the inner loop to start over
            
            attempts += 1
        
        if feedback == 'G' * len(guess):
            continue  # Start over if the word was guessed correctly
        else:
            print('Ops! Failed to guess the word.')
            break  # Exit the outer loop if the solver fails

# Main game loop to handle restarting the game with 'A'
while True:
    # Use a single URL that contains all words of various lengths
    word_list_url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'  # Replace with your actual link

    # Show introductory message and rules
    show_intro()

    # Ask the user for the word length
    word_length = int(input("Enter the length of the word: "))
    clear_console()


    # Fetch and filter the word list based on the user's input
    word_list = fetch_word_list(word_list_url, word_length)

    # Start the solver
    if word_list:
        wordle_solver(word_list)
    else:
        print(f"No words found with {word_length} letters. Please check the word list.")
