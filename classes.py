from collections import UserDict  # , Counter
import re
from abc import ABC, abstractmethod
import datetime

from typing import Any

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


'''class EmailExistException(Exception):
    def __init__(self, email_for_verification: str) -> None:
        self.message = f'Email {email_for_verification} already exists.'
        super().__init__(self.message)'''


class NameNotExistException(Exception):
    def __init__(self, name_for_verification: str) -> None:
        self.message = f'Name {name_for_verification} does not exist.'
        super().__init__(self.message)


class PhoneNotExistException(Exception):
    def __init__(self, number_for_verification: str) -> None:
        self.message = f'Number {number_for_verification} does not exist.'
        super().__init__(self.message)


'''class EmailNotExistException(Exception):
    def __init__(self, email_for_verification: str) -> None:
        self.message = f'Email {email_for_verification} does not exist.'
        super().__init__(self.message)'''


class BirthdayNotExistException(Exception):
    def __init__(self, message: str = 'Birthday does not exist for this contact.') -> None:
        self.message = message
        super().__init__(self.message)


class StatusNotExistException(Exception):
    def __init__(self, status_for_verification: str) -> None:
        self.message = f'Status {status_for_verification} does not exist.'
        super().__init__(self.message)


class RecordExistException(Exception):
    def __init__(self, record_for_verification: str) -> None:
        self.message = f'Record with a such name {record_for_verification} already exists.'
        super().__init__(self.message)


class RecordNotExistException(Exception):
    def __init__(self, record_for_verification: str) -> None:
        self.message = f'Record with a such name {record_for_verification} does not exist.'
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

    @abstractmethod
    def give_info(self):
        raise NotImplementedError


class UnnecessaryField(ABC):
    @abstractmethod
    def get_value(self):
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value):
        raise NotImplementedError

    @abstractmethod
    def give_info(self):
        raise NotImplementedError


class Name(Field):
    def __init__(self, name: str):
        self.__name = None
        self.set_value(name)

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

    def give_info(self) -> str:
        return '''\n\tA name of a contact.
        The field name cannot be empty.
        To change a name of some contact enter: change name <name of contact>'''


class Phone(Field):
    def __init__(self, phone_number: str) -> None:
        self.__phone_number = []
        _value = self._check_value(phone_number)
        if _value:
            self.__phone_number.append(_value)

    def get_value(self) -> list[str]:
        return self.__phone_number

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
        if _number and _number not in self.__phone_number:
            self.__phone_number.append(_number)
        elif not _number:
            raise PhoneNumberNotFilledException
        else:
            raise PhoneExistException(_number)

    def delete_phone_number(self, phone_number):
        if phone_number in self.__phone_number:
            self.__phone_number.remove(phone_number)
        raise PhoneNotExistException(phone_number)

    def give_info(self):
        return '''\n\tA phone number of a contact.
        All phone numbers should be added according to a phone pattern: +<code of a country>XXXXXXXXX or 
        <operator code>XXXXXXX
        All phone numbers are saved according to the pattern: +<code of a country>(XX)XXXXXXX
        
        To add a new phone number to some contact enter: add phone <name of a contact>
        To change a phone number of some contact enter: change phone <name of a contact>
        To delete a phone number of some contact enter: delete phone <name os a contact>'''


class Email(Field):
    def __init__(self, email: str = None) -> None:
        _value = self._check_value(email)
        self.__email = _value

    def get_value(self) -> str:
        return self.__email

    def set_value(self, new_email: str) -> None:
        self.__email = self._check_value(new_email)

    def _check_value(self, email: str) -> str | None | Exception:
        if email and re.match(r"([a-zA-Z.]+\w+\.?)+(@\w{2,}\.)(\w{2,})", email):
            return email
        elif not email:
            return None
        else:
            raise ValidEmailException(email)

    def give_info(self):
        return '''\n\tAn email of a contact.
        All emails should be written according to a valid format of your type of email.
        To change/add (if this field is empty) an email of some contact enter: change email <name of a contact>'''


class BirthDay(Field):
    def __init__(self, birth_date: str = None):
        _value = self._check_value(birth_date)
        self.__birth_date = _value

    def get_value(self) -> datetime.date:
        return self.__birth_date

    def set_value(self, birth_date_: str) -> None:
        self.__birth_date = self._check_value(birth_date_)

    def _check_value(self, birthday: str) -> datetime.date | None | Exception:
        if birthday:
            try:
                year, month, day = birthday.strip().split('-')
            except ValueError:
                raise ValidBirthDateException(birthday)
            try:
                return datetime.date(int(year), int(month), int(day))
            except ValueError:
                raise ValidBirthDateFormatException(birthday)
        else:
            return None

    def days_to_birthday(self) -> int:
        if self.__birth_date:
            current_date: datetime.date = datetime.date.today()
            birthday: datetime.date = datetime.date(year=current_date.year, month=self.__birth_date.month,
                                                    day=self.__birth_date.day)
            diff: int = (birthday - current_date).days
            if diff < 0:
                birthday = datetime.date(year=current_date.year + 1, month=self.__birth_date.month,
                                         day=self.__birth_date.day)
                diff = (birthday - current_date).days
            return diff
        raise BirthdayNotExistException

    def give_info(self):
        return'''\n\tA birthday of a contact.
        All dates of the birthday should be written according to the pattern: YYYY-MM-DD
        To change/add (if this field is empty) a date of birth of some contact enter: 
        change bd <name of a contact>
        To show how many days left to someone birthday enter: days to bd <name of a contact>'''


class Status(Field):
    def __init__(self, status: str = None):
        self.statuses = ['Friend', 'Family', 'Co-Worker', 'Special', None]
        _status = self._check_value(status)
        self.__status = _status

    def get_value(self) -> str:
        return self.__status

    def set_value(self, new_status: str) -> None:
        self.__status = self._check_value(new_status)

    def _check_value(self, status):
        if status in self.statuses:
            return status
        raise StatusNotExistException(status)

    def give_info(self):
        return '''\n\tA status of a contact.
        You can add one of the following statuses to your contact: Friend, Family, Co-Worker, Special.
        Or it can be empty.
        To add/change a status of some contact enter: change status <name of a contact>'''


class Note(UnnecessaryField):
    def __init__(self, note: str = None):
        self._note = note

    def get_value(self) -> str:
        return self._note

    def set_value(self, new_note: str):
        self._note = new_note

    def give_info(self):
        return '''\n\tA note of a contact.
        To add/change a notes of some contact enter: change note <name of a contact>
        Or it can be empty'''


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
        return ', '.join([f'{name}: {value.get_value()}' for name, value in vars(self).items()])

    def get_fields(self) -> dict:
        fields_dict: dict = {name: value.get_value() for (name, value) in vars(self).items()}
        return fields_dict

    @staticmethod
    def parser(element: Any) -> str:
        if isinstance(element, list):
            return ' '.join(element)
        elif isinstance(element, datetime.date):
            return element.strftime('%A %d %B %Y')
        elif isinstance(element, str):
            return element

    def search(self, parameter: str) -> str:
        data = self.get_fields()
        for value in data.values():
            if value and re.search(parameter, self.parser(value), flags=re.I):
                return value

    def get_all_info(self):
        return [info.give_info() for info in vars(self).values()]


class AddressBook(UserDict):
    start: int = 0

    def info(self):
        head = '''\n\tGeneral commands for all written contacts:
        To create a new contact enter: add contact <name of a new contact>
        To delete some contact enter: delete contact <name of a contact>
        To search a contact by a name or a phone or an email a date of birth or a status either a note, 
        using a full value of the field name or only a part of it, enter: search <keyword>
        To show all notices of an address book enter: show all'''
        foot = '''\n\tTo read all commands once again enter: help
    To exit and shut down the CUI assistant enter: good bye or close or exit
    Names, phone numbers, emails and other parameters have to be written without brackets <...>'''
        info_record = Record(Name('INFO'))
        help_ = info_record.get_all_info()
        help_.insert(0, head)
        help_.append(foot)
        return help_

    def add_record(self, record: Record) -> None:
        if record.name.get_value() in self.data:
            raise RecordExistException(record.name.get_value())
        self.data[record.name.get_value()] = record

    def delete_record(self, name: str) -> None:
        if name not in self.data:
            raise RecordNotExistException(name)
        del self.data[name]

    def iterator(self, page: int = 2):
        while True:
            data = list(self.data.values())[self.start: self.start+page]
            if not data:
                break
            yield data
            self.start += page

    def search_by_keyword(self, parameter: str):
        for record in self.data.values():
            if record.search(parameter):
                return record
        return 'There are not matches...'

    def search_by_name(self, name) -> list:
        # return [key if re.search(name, key, flags=re.I) else NameNotExistException(name) for key in self.data]
        for key in self.data:
            if re.search(name, key, flags=re.I):
                return key
        raise NameNotExistException(name)

    def __str__(self) -> dict:
        return self.data


contacts = AddressBook()

p = Name('I')
p.set_value('OK')
print(p.get_value())
n = Note('ok_')
print(n)
# p1 = Name('')

number = Phone('')
print(number.get_value())
eml = Email()
print(eml.get_value())
rec_ = Record(Name('Anton'), bd=BirthDay('1990-01-06'), status=Status('Friend'), note=Note('myself'))
print(rec_, 1)
print(rec_.search('ant'))
print('-' * 120)

rec_.note.set_value('it is me)')
print(rec_, 1)
rec = Record(p)
print(rec, 2)
rec.note.set_value('test')
print(rec, 2)
rec_.email.set_value('ah.hr@gmail.com')
print(rec_.email.get_value())
print(rec_, 1)
rec.status.set_value('Special')
print(rec, 2, '\n')

contacts.add_record(rec)
contacts.add_record(rec_)
print(contacts['Anton'].bd.days_to_birthday())
# print(contacts['OK'].bd.days_to_birthday())
# contacts.delete_record('OK')
for key_, val in contacts.items():
    print(key_, '|', val)
print()
for el in contacts.iterator():
    print(*el)

print('-' * 120)
print(contacts.search_by_keyword('tes'))

for raw in contacts.info():
    print(raw)

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
