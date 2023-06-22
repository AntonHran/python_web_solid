import re
from classes import AddressBook, Record, Name, contacts
import pickle
from typing import Callable
from functools import wraps


def input_error(func):
    @wraps(func)
    def inner_func(args):
        try:
            return func(args) if args else func()
        except (KeyError, ValueError, IndexError, TypeError) as error:
            print(f'''Error: {error}. Please check the accordance of the entered data to the requirements.
    And also a correctness of the entered name or/and phone number. And, of course, their existence.''')
        except Exception as exc:
            print(exc)
    return inner_func


def write_info_from_class(obj: AddressBook) -> None:
    with open('contacts.bin', 'wb') as fr:
        pickle.dump(obj, fr)


def read_info_from_file() -> AddressBook:
    with open('contacts.bin', 'rb') as fr:
        contacts_from_file: AddressBook = pickle.load(fr)
    return contacts_from_file


@input_error
def add_contact(name: str) -> None:
    """
    A name of a contact.
    The field name cannot be empty.
    To create a new contact, type: add contact <name of a new contact>"""
    name: Name = Name(name)
    record: Record = Record(name)
    contacts.add_record(record)
    write_info_from_class(contacts)


@input_error
def delete_contact(name: str) -> None:
    """
    To delete some contact, type: delete contact <name of a contact>"""
    contacts.delete_record(name)
    write_info_from_class(contacts)


@input_error
def search(keyword: str) -> None:
    """
    To search a contact by a name or a phone or an email a date of birth or a status either a note,
    using a full value of the field name or only a part of it, type: search <keyword>"""
    print(contacts.search_by_keyword(keyword))


def show_contacts() -> None:
    """
    To show all notices of an address book, type: show all"""
    contacts_download = read_info_from_file()
    for record in contacts_download.iterator():
        print('\n'.join(record))
        input('Press "Enter": ')


def instructions() -> None:
    print('\n\tGeneral commands for all written contacts:\n'
          '\tNames, phone numbers, emails and other parameters have to be written without brackets <...>')
    for command in methods.values():
        if command.__doc__:
            print(command.__doc__)


@input_error
def change_name(name: str) -> None:
    """
    To change the name of some contact, type: change name <name of contact>"""
    name: str = contacts.search_by_name(name)
    contact_data: Record = contacts.data[name]
    contacts.delete_record(name)
    new_name: str = input('Please enter a new name for the contact: ')
    contact_data.name.set_value(new_name)
    contacts.add_record(contact_data)
    write_info_from_class(contacts)


@input_error
def add_phone_number(name: str) -> None:
    """
    A phone number of a contact.
    All phone numbers should be added according to a phone pattern: +<code of a country>XXXXXXXXX or
    <operator code>XXXXXXX
    All phone numbers are saved according to the pattern: +<code of a country>(XX)XXXXXXX

    To add a new phone number to some contact, type: add phone <name of a contact>"""
    name = contacts.search_by_name(name)
    number: str = input('Please enter a phone number according to a phone pattern: +<code of a country>XXXXXXXXX '
                        'or <operator code>XXXXXXX: ')
    contacts.data[name].phone.set_value(number)
    write_info_from_class(contacts)


@input_error
def delete_phone_number(name: str) -> None:
    """
    To change a phone number of some contact, type: change phone <name of a contact>"""
    name = contacts.search_by_name(name)
    number: str = input('Please enter a number to delete: ')
    contacts.data[name].phone.delete_phone_number(number)
    write_info_from_class(contacts)


@input_error
def change_phone_number(name: str) -> None:
    """
    To change a phone number of some contact, type: change phone <name of a contact>"""
    name = contacts.search_by_name(name)
    phone_num: str = input('Enter <an old phone number>-<new phone number> for the contact: ')
    old, new = phone_num.strip().split('-')
    contacts.data[name].phone.delete_phone_number(old)
    contacts.data[name].phone.set_value(new)
    write_info_from_class(contacts)


@input_error
def change_email(name: str) -> None:
    """
    An email of a contact.
    All emails should be written according to a valid format of your email type.
    To change or add (if this field is empty), an email of some contact, type: change email <name of a contact>"""
    name = contacts.search_by_name(name)
    email: str = input('Please enter an email for the contact: ')
    contacts.data[name].email.set_value(email)
    write_info_from_class(contacts)


@input_error
def change_birthdate(name: str) -> None:
    """
    A birthday of a contact.
    All dates of the birthday should be written according to the pattern: YYYY-MM-DD
    To change/add (if this field is empty) a birthdate of some contact, type:
    change bd <name of a contact>"""
    name = contacts.search_by_name(name)
    birthdate: str = input('Please enter a date of birth for the contact according to pattern YYYY-MM-DD: ')
    contacts.data[name].bd.set_value(birthdate)
    write_info_from_class(contacts)


@input_error
def days_to_birthday(name: str) -> None:
    """
    To show how many days left to someone's birthday, type: days to bd <name of a contact>"""
    name = contacts.search_by_name(name)
    print(f'Number days to birthday for {name} is {contacts.data[name].bd.days_to_birthday()} days.')


@input_error
def change_status(name: str) -> None:
    """
    A status of a contact.
    You can add one of the following statuses to your contact: Friend, Family, Co-Worker, Special.
    Or it can be empty.
    To add/change a status of some contact, type: change status <name of a contact>"""
    name = contacts.search_by_name(name)
    status: str = input('Please enter one of statuses to this contact: '
                        'Friend, Family, Co-Worker, Special. Or leave it empty: ')
    contacts.data[name].status.set_value(status)
    write_info_from_class(contacts)


@input_error
def add_note(name: str) -> None:
    """
    A note of a contact.
    To add/change notes of some contact, type: change note <name of a contact>
    Or it can be empty."""
    name = contacts.search_by_name(name)
    note: str = input('Please enter a note for the contact: ')
    contacts.data[name].note.set_value(note)
    write_info_from_class(contacts)


def greeting(object_: AddressBook):

    print('\n\tNow you are in your personal addressbook.\n'
          '\tI can help you with adding, changing, showing and storing all contacts and data connected with them.')
    try:
        object_.data.clear()
        [contacts.add_record(value) for value in read_info_from_file().values()]
        # contacts = read_info_from_file()
    except (FileExistsError, FileNotFoundError):
        print('There are not records yet. Your addressbook is empty.')


def farewell() -> None:
    """
    To exit the addressbook and come back to the main menu, type: back
    """
    write_info_from_class(contacts)
    print('All changes saved successfully.\n'
          '\nYou returned to the main Menu.')


methods = {'add contact': add_contact, 'delete contact': delete_contact, 'search': search,
           'show all': show_contacts, 'change name': change_name, 'add phone': add_phone_number,
           'change phone': change_phone_number, 'delete phone': delete_phone_number, 'change email': change_email,
           'change bd': change_birthdate, 'days to bd': days_to_birthday, 'change status': change_status,
           'add note': add_note, 'help': instructions, }


@input_error
def command_parser(command: str) -> tuple:
    for func in methods:
        if re.search(func, command, flags=re.I):
            return func, re.sub(func, '', command, flags=re.I).strip()


def handler(function_name: str) -> type[Callable]:
    return methods[function_name]


def address_book_main():
    greeting(contacts)
    instructions()
    while True:
        text: str = input('\nEnter your command: ')
        if text == 'back':
            farewell()
            break
        try:
            command, argument = command_parser(text)
            func = handler(command)
            func(argument) if argument else func()
        except (TypeError, KeyError):
            print('I do not understand what you want to do. Please look at the commands.')


'''if __name__ == '__main__':
    pass'''
