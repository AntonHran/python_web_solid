from collections import UserDict  # , Counter
import re
from abc import ABC, abstractmethod
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


class Field(ABC):
    @abstractmethod
    def __getitem__(self):
        raise NotImplementedError

    @abstractmethod
    def __setitem__(self, val):
        raise NotImplementedError

    @abstractmethod
    def _check_value(self, value):
        raise NotImplementedError


class UnnecessaryField(ABC):
    @abstractmethod
    def value_of(self):
        raise NotImplementedError


class Name(Field):
    def __init__(self, name: str):
        _value = self._check_value(name)
        if _value:
            self.__name = _value

    def __getitem__(self) -> str:
        return self.__name

    def __setitem__(self, newname: str):
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
        _value = self._check_value(phone_number)
        self.phone_number = []
        self.phone_number.append(_value)

    def __getitem__(self) -> list[str]:
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

    def __setitem__(self, phone_number: str):
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
    def __init__(self, email: str | None = None):
        _value = self._check_value(email)
        self.email = _value

    def __getitem__(self):
        return self.email

    def __setitem__(self, new_email: str) -> None:
        self.email = self._check_value(new_email)

    def _check_value(self, email: str) -> str | None | Exception:
        if email and re.match(r"([a-zA-Z.]+\w+\.?)+(@\w{2,}\.)(\w{2,})", email):
            return email
        elif not email:
            return None
        else:
            raise ValidEmailException


class BirthDay(Field):
    def __init__(self, birth_date: str):
        _value = self._check_value(birth_date)
        self.birth_date = _value

    def __getitem__(self):
        return self.birth_date

    def __setitem__(self, val):
        ...

    def _check_value(self, birthday):
        if birthday:
            return birthday
        elif not birthday:
            return None
        else:
            raise ValidBirthDateException


class Status(Field):
    def __init__(self, status: str):
        self.statuses = ['Friend', 'Family', 'Co-Worker', 'Special']
        _status = self._check_value(status)
        self.status = _status

    def __getitem__(self):
        return self.status

    def __setitem__(self, new_status: str) -> None:
        self.status = self._check_value(new_status)

    def _check_value(self, status):
        if status in self.statuses:
            return status
        return None


class Note(UnnecessaryField):
    def __init__(self, note: str):
        self.note = note

    def value_of(self):
        return self.note


class Record:
    def __init__(self, name: Field, phone: Field = None, email: Field = None,
                 bd: Field = None, status: Field = None, note: UnnecessaryField = None):
        self.name = name
        self.phone = Phone('') if not phone else phone
        self.email = Email() if not email else email
        self.bd = BirthDay('') if not bd else bd
        self.status = Status('') if not status else status
        self.note = Note('') if not note else note
        # self.lst = [self.phone, self.email, self.bd, self.status, self.note]

    def get_record(self):
        return f'name: {self.name.__getitem__()}, phone: {self.phone.__getitem__()}, ' \
               f'email: {self.email.__getitem__()}, birthday: {self.bd.__getitem__()}, ' \
               f'status: {self.status.__getitem__()}, note: {self.note.value_of()}.'


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.__getitem__()] = record


p = Name('I')
p.__setitem__('OK')
print(p.__getitem__())
# p1 = Name('')

number = Phone('')
print(number.__getitem__())
eml = Email('')
print(eml.__getitem__())
rec_ = Record(Name('Anton'), bd=BirthDay('1990-01-06'), status=Status('Friend'), note=Note('myself'))
print(rec_.get_record())
rec = Record(p)
print(rec.get_record())
rec_.email.__setitem__('ah.hr@gmail.com')
print(rec_.email.__getitem__())
print(rec_.get_record())
rec.status.__setitem__('Special')
print(rec.get_record())

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
