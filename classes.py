from collections import UserDict  # , Counter
import re
from abc import ABC, abstractmethod
import datetime
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
        self.message = f'Birth date {birth_date_for_verification} does not valid.'
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
        self.message = f'Name {name_for_verification} does not exist.'
        super().__init__(self.message)


class PhoneNotExistException(Exception):
    def __init__(self, number_for_verification: str) -> None:
        self.message = f'Number {number_for_verification} already exists.'
        super().__init__(self.message)


class EmailNotExistException(Exception):
    def __init__(self, email_for_verification: str) -> None:
        self.message = f'Email {email_for_verification} already exists.'
        super().__init__(self.message)


class StatusNotExistException(Exception):
    def __init__(self, status_for_verification: str) -> None:
        self.message = f'Status {status_for_verification} does not exist.'
        super().__init__(self.message)


class Field(ABC):
    @abstractmethod
    def get_value(self):
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value):
        raise NotImplementedError

    @abstractmethod
    def _check_value(self, value):
        raise NotImplementedError


class UnnecessaryField(ABC):
    @abstractmethod
    def get_value(self):
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value):
        raise NotImplementedError


class Name(Field):
    def __init__(self, name: str):
        _value = self._check_value(name)
        if _value:
            self.__name = _value

    def get_value(self) -> str:
        return self.__name

    def set_value(self, newname: str) -> None:
        _value = self._check_value(newname)
        if _value:
            self.__name = _value

    def _check_value(self, name: str) -> str | Exception:
        if name and isinstance(name, str):
            return name
        else:
            raise NameNotFilledException


class Phone(Field):
    def __init__(self, phone_number: str) -> None:
        self.phone_number = []
        _value = self._check_value(phone_number)
        if _value:
            self.phone_number.append(_value)

    def get_value(self) -> list[str]:
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

    def set_value(self, phone_number: str) -> None:
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
    def __init__(self, email: str = None) -> None:
        _value = self._check_value(email)
        self.email = _value

    def get_value(self) -> str:
        return self.email

    def set_value(self, new_email: str) -> None:
        self.email = self._check_value(new_email)

    def _check_value(self, email: str) -> str | None | Exception:
        if email and re.match(r"([a-zA-Z.]+\w+\.?)+(@\w{2,}\.)(\w{2,})", email):
            return email
        elif not email:
            return None
        else:
            raise ValidEmailException


class BirthDay(Field):
    def __init__(self, birth_date: str = None):
        _value = self._check_value(birth_date)
        self.birth_date = _value

    def get_value(self) -> datetime.date:
        return self.birth_date

    def set_value(self, birth_date_: str) -> None:
        self.birth_date = self._check_value(val)

    def _check_value(self, birthday: str) -> datetime.date | None | Exception:
        if birthday:
            year, month, day = birthday.strip().split('-')
            return datetime.date(int(year), int(month), int(day))
        elif not birthday:
            return None
        else:
            raise ValidBirthDateException


class Status(Field):
    def __init__(self, status: str = None):
        self.statuses = ['Friend', 'Family', 'Co-Worker', 'Special', None]
        _status = self._check_value(status)
        self.status = _status

    def get_value(self) -> str:
        return self.status

    def set_value(self, new_status: str) -> None:
        self.status = self._check_value(new_status)

    def _check_value(self, status):
        if status in self.statuses:
            return status
        raise StatusNotExistException(status)


class Note(UnnecessaryField):
    def __init__(self, note: str = None):
        self.note = note

    def get_value(self) -> str:
        return self.note

    def set_value(self, note: str):
        self.note = note


class Record:
    def __init__(self, name: Field, phone: Field = None, email: Field = None,
                 bd: Field = None, status: Field = None, note: UnnecessaryField = None) -> None:
        self.name = name
        self.phone = Phone('') if not phone else phone
        self.email = Email() if not email else email
        self.bd = BirthDay() if not bd else bd
        self.status = Status() if not status else status
        self.note = Note() if not note else note

    def __str__(self) -> str:
        return f'name: {self.name.get_value()}, phone: {self.phone.get_value()}, ' \
               f'email: {self.email.get_value()}, birthday: {self.bd.get_value()}, ' \
               f'status: {self.status.get_value()}, note: {self.note.get_value()}.'


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.get_value()] = record

    def delete_record(self, name: str) -> None:
        del self.data[name]

    def iter(self):
        ...

    def search(self):
        ...

    def __str__(self) -> dict:
        return self.data


contacts = AddressBook()

p = Name('I')
p.set_value('OK')
print(p.get_value())
# p1 = Name('')

number = Phone('')
print(number.get_value())
eml = Email('')
print(eml.get_value())
rec_ = Record(Name('Anton'), bd=BirthDay('1990-01-06'), status=Status('Friend'), note=Note('myself'))
print(rec_.__str__(), 1)
rec_.note.set_value('it is me)')
print(rec_.__str__(), 1)
rec = Record(p)
print(rec.__str__(), 2)
rec.note.set_value('test')
print(rec.__str__(), 2)
rec_.email.set_value('ah.hr@gmail.com')
print(rec_.email.get_value())
print(rec_.__str__(), 1)
rec.status.set_value('Special')
print(rec.__str__(), 2, '\n')

contacts.add_record(rec)
contacts.add_record(rec_)
# contacts.delete_record('OK')
for key, val in contacts.__str__().items():
    print(key, val.__str__())

'''lst = [2, 3, 4, 5, 2, 6, 3, 9, 10, 11, 2]
counts = Counter(lst)
origin = [key for key in counts if counts[key] == 1]
print(origin)

orig = []
for el in lst:
    copy = [*lst]
    copy.remove(el)
    if el not in copy:
        orig.append(el)
print(orig)

org = []
for el in lst:
    k = 0
    for el_1 in lst:
        if el == el_1:
            k += 1
    if k == 1:
        org.append(el)
print(org)'''
