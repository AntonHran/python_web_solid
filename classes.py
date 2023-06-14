from collections import UserDict
import re
# from typing import *

UKR_MOBILE_PHONE_CODES = ['095', '099', '050', '063', '066', '067', '077', '0800', '045', '046', '032',
                          '044', '048', '068', '097', '098', '091', '092', '094', ]


class NameNotFilledException(Exception):
    def __init__(self, message='Name can not be missing/empty.') -> None:
        self.message = message
        super().__init__(self.message)


class PhoneNumberNotFilledException(Exception):
    def __init__(self, message='You can not add empty value as a phone number!!!') -> None:
        self.message = message
        super().__init__(self.message)


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

    def _check_value(self, value):
        raise NotImplementedError


class UnnecessaryField:
    def value_of(self):
        raise NotImplementedError


class Name(Field):
    def __init__(self, name: str):
        _value = self._check_value(name)
        if _value:
            self.__name = _value

    def value_of(self) -> str:
        return self.__name

    def set_name(self, newname: str):
        _value = self._check_value(newname)
        if _value:
            self.__name = _value

    def _check_value(self, name: str) -> str | Exception:
        if name and isinstance(name, str):
            return name
        else:
            raise NameNotFilledException


class Phone(Field):
    def __init__(self, phone_number: str | None) -> None:
        _value = self._check_value(phone_number)
        self.phone_number = []
        self.phone_number.append(_value)

    def value_of(self) -> list[str]:
        return self.phone_number

    def _check_value(self, phone_num) -> str | None | Exception:
        if phone_num:
            phone_num = re.sub(r'[+\-() ]', '', phone_num)
            if re.fullmatch(r'^([0-9]){6,14}[0-9]$', phone_num):
                for inner_code in UKR_MOBILE_PHONE_CODES:
                    if phone_num.startswith(inner_code):
                        return f'+38{phone_num}'
            else:
                raise ValidPhoneException(phone_num)
        return None

    def add_phone_number(self, phone_number: str):
        _number = self._check_value(phone_number)
        if _number and _number not in self.phone_number:
            self.phone_number.append(_number)
        elif not _number:
            raise PhoneNumberNotFilledException
        else:
            raise PhoneExistException(_number)

    def __str__(self) -> str:
        return f'Info: telephone number(-s): {", ".join(self.phone_number)}'


class Email(Field):
    def __init__(self, email: str | None):
        _value = self._check_value(email)
        self.email = _value

    def value_of(self):
        return self.email

    def _check_value(self, email: str) -> str | None | Exception:
        if email and re.match(r"([a-zA-Z.]+\w+\.?)+(@\w{2,}\.)(\w{2,})", email):
            return email
        elif not email:
            return None
        else:
            raise ValidEmailException


class BirthDay(Field):
    def __init__(self, birth_date: str | None):
        _value = self._check_value(birth_date)
        self.birth_date = _value

    def value_of(self):
        return self.birth_date

    def _check_value(self, birthday):
        if birthday:
            return birthday
        else:
            raise ValidBirthDateException


class Status(UnnecessaryField):
    def __init__(self, status: str):
        self.status = status

    def value_of(self):
        return self.status


class Note(UnnecessaryField):
    def __init__(self, note: str):
        self.note = note

    def value_of(self):
        return self.note


class Record:
    def __init__(self, name: Field, phone: Field | None = None, email: Field | None = None,
                 bd: Field | None = None, status: Field | None = None, note: UnnecessaryField | None = None):
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


p = Name('I')
p.set_name('OK')
print(p.value_of())
# p1 = Name('')

number = Phone(None)
print(number.value_of())
eml = Email(None)
print(eml.value_of())
rec = Record(p, number, eml)
print(rec.get_record())
