'''Реалізація класів для управління адресною книгою'''

from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
from collections import UserDict


class Field(ABC):
    '''Абстрактний клас для полів запису.'''

    def __init__(self, value):
        self._value = None
        self.value = value

    @abstractmethod
    def validate(self, value):
        '''Абстрактний метод для валідації значення.'''
        pass

    @property
    def value(self):
        '''Доступ до поля класу через гетер'''
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def __str__(self):
        return str(self.value)


class Name(Field):
    '''Клас для зберігання імені контакту.'''

    def validate(self, value: str):
        if not value.strip():
            raise AddressBookValueError("Name must be a non-empty string.")


class Phone(Field):
    '''Клас для зберігання номера телефону.'''

    def validate(self, value: str):
        if not (value.isdigit() and len(value) == 10):
            raise AddressBookValueError("Phone number must contain exactly 10 digits.")


class Birthday(Field):
    '''Клас для зберігання дня народження.'''

    def validate(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise AddressBookValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    '''Клас для зберігання інформації про контакт, включаючи ім'я, 
    список телефонів та дату народження.
    '''

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday: str):
        '''Метод додавання дати народження'''
        self.birthday = Birthday(birthday)

    def add_phone(self, phone_number: str):
        '''Метод додавання номеру телефону'''
        if self.find_phone(phone_number) is None:
            self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str):
        '''Метод видалення номеру телефону'''
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_number: str, new_number: str):
        '''Метод редагування номеру телефону'''
        phone = self.find_phone(old_number)
        if phone:
            phone.value = new_number
        else:
            raise AddressBookValueError(f"Phone number {old_number} not found!")

    def find_phone(self, phone_number: str):
        '''Метод пошуку номеру телефону'''
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        result = f"Contact name: {self.name.value}, phones: {'; '.join(p.value
                                                            for p in self.phones)}"
        if self.birthday:
            result += f", birthday: {self.birthday.value}"
        return result


class AddressBook(UserDict):
    '''Клас для зберігання та управління записами.'''
    def add_record(self, record: Record):
        '''Метод додавання запису до адресної книги'''
        if self.find(record.name.value) is None:
            self.data[record.name.value] = record


    @staticmethod
    def string_to_date(date_string: str):
        '''Метод перетворює рядок з датою в об'єкт datetime'''
        return datetime.strptime(date_string, "%d.%m.%Y").date()


    @staticmethod
    def adjust_for_weekend(birthday):
        '''Якщо дата народження випадає на вихідний, метод повертає
        дату наступного понеділка
        '''
        if birthday.weekday() >= 5:
            return AddressBook.find_next_weekday(birthday, 0)
        return birthday


    @staticmethod
    def find_next_weekday(start_date, weekday):
        '''Метод дозволяє знайти дату наступного конкретного дня тижня
        після заданої дати
        '''
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)


    def get_upcoming_birthdays(self, days=7):
        '''Метод визначає контакти, у яких день народження припадає
        вперед на 7 днів включаючи поточний день.
        '''
        upcoming_birthdays = []
        today = date.today()

        for name in self.data:
            if self.data[name].birthday:
                birthday_this_year = \
                    AddressBook.string_to_date(
                        self.data[name].birthday.value).replace(year=today.year)
                # Перевірка, чи не буде
                # припадати день народження вже наступного року.
                if birthday_this_year < today:
                    birthday_this_year = \
                        AddressBook.string_to_date(
                            self.data[name].birthday.value).replace(year=today.year+1)

                if 0 <= (birthday_this_year - today).days <= days:
                    # Перенесення дати привітання на наступний робочий день,
                    # якщо день народження припадає на вихідний.
                    birthday_this_year = AddressBook.adjust_for_weekend(birthday_this_year)

                    congratulation_date_str = birthday_this_year.strftime("%d.%m.%Y")
                    upcoming_birthdays.append({
                        "name": self.data[name].name.value,   
                        "congratulation_date": congratulation_date_str
                        })
        return upcoming_birthdays


    def find(self, name: str):
        '''Метод пошуку запису за ім'ям'''
        return self.data.get(name)


    def delete(self, name: str):
        '''Метод видалення запису за ім'ям'''
        self.data = {key: self.data[key] for key in self.data if key != name}


    def __str__(self):
        return f"{'\n'.join(self.data[k].__str__() for k in self.data)}"


class AddressBookValueError(ValueError):
    '''Клас винятку для адресної книги'''
    pass
