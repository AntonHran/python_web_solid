import random
import re
from illustration_to_game import draw


def choose() -> tuple:
    word_list: list = ['python', 'java', 'swift', 'javascript', 'ruby', 'html', 'php']
    word: str = random.choice(word_list)
    gues_word: str = '-' * len(word)
    return word, gues_word


def game() -> tuple:
    word, gues_word = choose()
    i: int = 0
    entered_letters: str = ''
    while i < 8 and gues_word != word:
        print('\n' + gues_word)
        letter: str = input('Input a letter: ')
        letter = check_enter(letter)
        if letter:
            entered_letters += letter
            if entered_letters.count(letter) > 1:
                print("You have already guessed this letter.")
            elif letter in word:
                gues_word = show_changes(word, letter, gues_word)
            else:
                print(f"The letter {letter} doesn't present in the word.")
                i += 1
                draw(i)
    win, lose = result(word, gues_word)
    return win, lose


def result(word: str, guested_word: str) -> tuple:
    win, lose = 0, 0
    if word != guested_word:
        print('\nYou lost!')
        lose = 1
    else:
        print(f'\nYou guessed the word: {word}! \nYou survived!')
        win = 1
    return win, lose


def show_changes(wrd: str, let: str, str_: str) -> str:
    str_: list = list(str_)
    for i in range(len(wrd)):
        if wrd[i] == let:
            str_[i] = wrd[i]
    return ''.join(str_)


def check_enter(let: str) -> str:
    pattern = re.compile(r'\b[a-z]\b')
    matches = re.search(pattern, let)
    if matches:
        return let
    elif len(let) == 1 and (let.isupper() or let.isascii()):
        print('Please, enter a lowercase letter from the English alphabet.')
    else:
        print('Please, input a single letter.')


def game_main():
    print('''\tH A N G M A N
    This is entertainment module with a well known game - hangman. So are you ready gues a word?\n
    Type "play" to play the game, "score" to show the scoreboard, and "back" to return to main menu.''')
    win_total = 0
    lose_total = 0
    while True:
        answer = input('\nMake your choice: ')
        if answer == 'play':
            win, lose = game()
            win_total += win
            lose_total += lose
        elif answer == 'score':
            print(f'\nYou won: {win_total} times.\nYou lost: {lose_total} times.')
        elif answer == 'back':
            print('\nYou returned to the main Menu.')
            break
