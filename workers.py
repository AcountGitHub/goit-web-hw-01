'''Абстрактні класи для роботи із записами адресної книги та їх реалізації'''

import pickle
from abc import ABC, abstractmethod
from contacts import AddressBook, Record

class BotWorker(ABC):
    '''Абстрактний клас для роботи із записами адресної книги'''
    def __init__(self, book: AddressBook):
        self.book = book

    @abstractmethod
    def update(self, args):
        '''Абстрактний метод для оновлення значень'''
        pass

    @abstractmethod
    def show(self, args):
        '''Абстрактний метод для повернення значень'''
        pass


class ContactWorker(BotWorker):
    '''Клас реалізовує оновлення та повернення записів в адресній книзі.'''

    def update(self, args):
        '''Метод оновлення записів в адресній книзі. В залежності від
        отриманих аргументів створюється новий контакт або до існуючого
        запису додається новий номер телефону.'''
        name, phone, *_ = args
        record = self.book.find(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            self.book.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        return message

    def show(self, args=None):
        '''Метод повертає всі записи в адресній книзі'''
        return str(self.book)


class PhonesWorker(BotWorker):
    '''Клас реалізовує оновлення та повернення телефонних номерів для
    вказаного контакту
    '''
    def update(self, args):
        '''Метод оновлення номеру телефону для вказаного контакту.'''
        message = "Contact updated."
        name, old_phone, new_phone, *_ = args
        record = self.book.find(name)
        if record:
            record.edit_phone(old_phone, new_phone)
        else:
            message = f"Contact with name {name} not found!"
        return message

    def show(self, args):
        '''Метод повертає телефонні номери для контакту з заданим ім'ям.'''
        return ", ".join(phone.value for phone in self.book[args[0]].phones)


class BirthdayWorker(BotWorker):
    '''Клас реалізовує оновлення та повернення дня народження для
    вказаного контакту
    '''
    def update(self, args):
        '''Метод оновлює дату народження для вказаного контакту.'''
        name, birthday, *_ = args
        record = self.book.find(name)
        message = "Birthday added."
        if record:
            if record.birthday:
                message = "Birthday updated."
            record.add_birthday(birthday)
        else:
            message = f"Contact with name {name} not found!"
        return message

    def show(self, args):
        '''Метод повертає дату народження для вказаного контакту'''
        if self.book[args[0]].birthday:
            return self.book[args[0]].birthday.value
        else:
            return f"Birthday for contact with name {args[0]} not found!"

    def show_upcoming_birthdays(self):
        '''Метод повертає список контактів, яких потрібно привітати по днях
        на наступному тижні
        '''
        upcoming_birthdays = self.book.get_upcoming_birthdays()
        return f"{'\n'.join(b['name'] + ": " + b['congratulation_date']
                            for b in upcoming_birthdays)}"


class FileWorker(ABC):
    '''Інтерфейс відновлення даних з файлу та їх збереження в файл'''

    @abstractmethod
    def load_data(self):
        '''Абстрактний метод відновлення з файлу'''
        pass

    @abstractmethod
    def save_data(self, data):
        '''Абстрактний метод збереження в файл'''
        pass


class PickleWorker(FileWorker):
    '''Реалізація інтерфейсу з використанням pickle'''

    def load_data(self, filename="addressbook.pkl"):
        '''Метод відновлення адресної книги з файлу'''
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            # Повернення нової адресної книги, якщо файл не знайдено
            return AddressBook()

    def save_data(self, data: AddressBook, filename="addressbook.pkl"):
        '''Метод збереження адресної книги в файл'''
        with open(filename, "wb") as f:
            pickle.dump(data, f)
