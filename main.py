from functions import address_book_main
from cleaner_functions import clean_folder_main
from game import game_main
import asyncio

main_ = {1: address_book_main, 2: clean_folder_main, 3: game_main, }

if __name__ == '__main__':
    while True:
        choice = int(input('Please make your choice: '))
        if choice == 0:
            print('Good bye)')
            break
        main_[choice]() if choice != 2 else asyncio.run(main_[choice]())
