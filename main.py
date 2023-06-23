from functions import address_book_main
from cleaner_functions import clean_folder_main
from game import game_main
import asyncio


def main_instructions() -> None:
    print('''\n\t1. addressbook with your contacts, 
    2. cleaning block where I can sort your files and 
    3. gaming block for a bit of entertainment.\n
    To choice the block, just enter its number 1, 2 or 3 in the offered field.\n
    To see instructions of main menu, type 4.
    To close the personal assistant, enter 0''')


main_ = {1: address_book_main, 2: clean_folder_main, 3: game_main, 4: main_instructions}


if __name__ == '__main__':
    print('''\tWelcome to the CUI personal assistant.
    Here I have my Main menu. It consists of three blocks: ''')
    main_instructions()
    while True:
        choice = int(input('\nPlease make your choice: '))
        if choice == 0:
            print('\nGood bye)')
            break
        main_[choice]() if choice != 2 else asyncio.run(main_[choice]())
#------