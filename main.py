from functions import greeting, instructions, command_parser, handler


def main():
    greeting()
    instructions()
    while True:
        text: str = input('\nEnter your command: ')
        try:
            command, argument = command_parser(text)
            func = handler(command)
            func(argument) if argument else func()
        except (TypeError, KeyError):
            print('I do not understand what you want to do. Please look at the commands.')


if __name__ == '__main__':
    main()
