from collections import UserDict
# from typing import *


class ValidPhoneException(Exception):
    def __init__(self, number_for_validation: str) -> None:
        self.message = f'Wrong format of {number_for_validation}.'
        super().__init__(self.message)


class ValidEmailException(Exception):
    def __init__(self, email_for_validation: str) -> None:
        self.message = f'Wrong format of {email_for_validation}.'
        super().__init__(self.message)


class ValidBirthDateException(Exception):
    def __init__(self, birth_date_for_validation: str) -> None:
        self.message = f'Wrong format of {birth_date_for_validation}.'
        super().__init__(self.message)


class ValidBirthDateFormatException(Exception):
    def __init__(self, birth_date_for_verification: str) -> None:
        self.message = f'Birth date {birth_date_for_verification} is not valid.'
        super().__init__(self.message)


class PhoneExistException(Exception):
    def __init__(self, number_for_verification: str) -> None:
        self.message = f'Number {number_for_verification} already exists.'
        super().__init__(self.message)


class EmailExistException(Exception):
    def __init__(self, email_for_verification: str) -> None:
        self.message = f'Email {email_for_verification} already exists.'
        super().__init__(self.message)


class NameNotExistException(Exception):
    def __init__(self, name_for_verification: str) -> None:
        self.message = f'Name {name_for_verification} is not exist.'
        super().__init__(self.message)


class PhoneNotExistException(Exception):
    def __init__(self, number_for_verification: str) -> None:
        self.message = f'Number {number_for_verification} already exists.'
        super().__init__(self.message)


class EmailNotExistException(Exception):
    def __init__(self, email_for_verification: str) -> None:
        self.message = f'Email {email_for_verification} already exists.'
        super().__init__(self.message)


class Field:
    def value_of(self):
        raise NotImplementedError

    def check_value(self, value):
        raise NotImplementedError


class Name(Field):
    def __init__(self, name: str):
        _value = self.check_value(name)
        self.__name = _value

    def value_of(self):
        return self.__name

    def set_name(self, newname):
        self.__name = newname

    def check_value(self, name):
        if name:
            return name
        else:
            raise ValueError


class Phone(Field):
    def __init__(self, phone_number: str):
        _value = self.check_value(phone_number)
        self.phone_number = [_value]

    def value_of(self):
        return self.phone_number

    def check_value(self, phone_num):
        if phone_num:
            return phone_num


class Email(Field):
    def __init__(self, email: str):
        _value = self.check_value(email)
        self.email = _value

    def value_of(self):
        return self.email

    def check_value(self, email: str) -> str:
        if email:
            return email


class BirthDay(Field):
    def __init__(self, birth_date: str):
        _value = self.check_value(birth_date)
        self.birth_date = _value

    def value_of(self):
        return self.birth_date

    def check_value(self, birthday):
        if birthday:
            return birthday


class Status(Field):
    def __init__(self, status: str):
        self.status = status

    def value_of(self):
        return self.status


class Note(Field):
    def __init__(self, note: str):
        self.note = note

    def value_of(self):
        return self.note


class Record:
    def __init__(self, name: Field, phone: Field | None, email: Field | None, bd: Field | None,
                 status: Field | None, note: Field | None):
        self.name = name
        self.phone = phone
        self.email = email
        self.bd = bd
        self.status = status
        self.note = note

    def get_record(self):
        return f'name: {self.name.value_of()}, phone: {self.phone.value_of()}, ' \
               f'email: {self.email.value_of()}, birthday: {self.bd.value_of()}, ' \
               f'status: {self.status.value_of()}, note: {self.note.value_of()}.'


class AddressBook(UserDict):
    # def __init__(self, record: Record):
    # super().__init__()
    # self.data[record.name.value_of()] = record
    def add_record(self, record: Record):
        self.data[record.name.value_of()] = record
