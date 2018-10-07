#!/usr/bin/python3
import random
import requests
import json
import random
import os

def main():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as f:
            data = json.load(f)
    except json.decoder.JSONDecodeError:
        print("\nAn error occurred while parsing settings.json!")
        return
    except FileNotFoundError:
        print("\nsettings.json was not found!")
        return
    except:
        print("\nsAn error occurred while attempting to read settings.json!")
        return
    welcome = [ '',
                'Welcome to Hangman! A word will be chosen at random and',
                'you must try to guess the word correctly letter by letter',
                'before you run out of attempts. Good luck!'
               ]
    for line in welcome:
        print(line, sep='\n')
    play_again = True

    while play_again:
        if data['UseLocalWordlistInsteadOfLinks']:
            files = []
            for (dirpath, dirnames, filenames) in os.walk(os.path.dirname(os.path.realpath(__file__)) + "/" + data['WordlistFolderName']):
                files.extend(filenames)
                break
            try:
                category = random.choice(files)
            except IndexError:
                print("\nNo files found in wordlists folder!")
                return
            categoryextension = '.' + category.split('.')[-1]
            category = ".".join(category.split('.')[:-1])
            try:
                with open("./" + data['WordlistFolderName'] + "/" + category + categoryextension) as f:
                    temp = f.read()
                    if temp[:7].lower() == '!!!del:':
                        delimiter = temp.split('\n')[0][7:].strip()
                    elif categoryextension == '.csv':
                        delimiter = ','
                    else:
                        delimiter = data['LocalFileDelimiter']

                    words = list(filter(None, temp.split(delimiter)))
            except:
                print("\nAn error occurred while attempting to read wordlist!")
                return
        else:
            wordset = random.choice(list(data['wordlist'].items()))
            category = wordset[0]
            wordpage = wordset[1][0]
            try:
                words = requests.get(wordpage).text.split(wordset[1][1])
            except:
                print("\nAn error occurred while reading wordlists. Check your internet connection and try again!")
                return
        print(("\nThe category of your word is: {}".format(category)))
        chosen_word = random.choice(words).lower().strip()
        player_guess = None 
        guessed_letters = []
        word_guessed = []
        for letter in chosen_word:
            word_guessed.append("-")
        joined_word = None
        HANGMAN = (
"""
-----
|   |
|
|
|
|
|
|
|
--------
""",
"""
-----
|   |
|   0
|
|
|
|
|
|
--------
""",
"""
-----
|   |
|   0
|  -+-
|
|
|
|
|
--------
""",
"""
-----
|   |
|   0
| /-+-
|
|
|
|
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|
|
|
|
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|   | 
|
|
|
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|   | 
|   | 
|
|
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|   | 
|   | 
|  |
|
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|   | 
|   | 
|  | 
|  | 
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|   | 
|   | 
|  | | 
|  | 
|
--------
""",
"""
-----
|   |
|   0
| /-+-\ 
|   | 
|   | 
|  | | 
|  | | 
|
--------
""")
        print(HANGMAN[0])
        attempts = len(HANGMAN) - 1
        while (attempts != 0 and "-" in word_guessed):
            print(("\nYou have {} attempts remaining").format(attempts))
            joined_word = "".join(word_guessed)
            print(joined_word)
            try:
                print(("\n[{}]").format(''.join(guessed_letters).upper()))
                player_guess = str(input("\nPlease select a letter between A-Z" + "\n> ")).lower()
            except:
                print("That is not valid input. Please try again.")
                continue                
            else: 
                if not player_guess.isalpha():
                    print("That is not a letter. Please try again.")
                    continue
                elif len(player_guess) > 1:
                    print("That is more than one letter. Please try again.")
                    continue
                elif player_guess in guessed_letters:
                    print("You have already guessed that letter. Please try again.")
                    continue
                else:
                    pass
            guessed_letters.append(player_guess)
            for letter in range(len(chosen_word)):
                if player_guess == chosen_word[letter]:
                    word_guessed[letter] = player_guess
            if player_guess not in chosen_word:
                attempts -= 1
                print(HANGMAN[(len(HANGMAN) - 1) - attempts])
        if "-" not in word_guessed:
            print(("\nCongratulations! {} was the word").format(chosen_word))
        else:
            print(("\nUnlucky! The word was {}.").format(chosen_word))
        print("\nWould you like to play again?")
        response = input("> ").lower()
        if response not in ("yes", "y"):
            play_again = False

if __name__ == "__main__":
    main()