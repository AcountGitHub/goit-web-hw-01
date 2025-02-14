'''Інтерфейс для роботи із записами адресної книги та його реалізації'''

from abc import ABC, abstractmethod
from contacts import AddressBook, Record

class BotWorker(ABC):
    '''Загальний інтерфейс для роботи із записами адресної книги'''
    @abstractmethod
    def update(self, args, book: AddressBook):
        '''Абстрактний метод для оновлення значень'''
        pass

    @abstractmethod
    def show(self, args, book: AddressBook):
        '''Абстрактний метод для повернення значень'''
        pass


class ContactWorker(BotWorker):
    '''Клас реалізовує оновлення та повернення записів в адресній книзі.'''

    def update(self, args, book: AddressBook):
        '''Метод оновлення записів в адресній книзі. В залежності від
        отриманих аргументів створюється новий контакт або до існуючого
        запису додається новий номер телефону.'''
        name, phone, *_ = args
        record = book.find(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            book.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        return message

    def show(self, _, book: AddressBook):
        '''Метод повертає всі записи в адресній книзі'''
        return str(book)


class PhonesWorker(BotWorker):
    '''Клас реалізовує оновлення та повернення телефонних номерів для
    вказаного контакту
    '''
    def update(self, args, book: AddressBook):
        '''Метод оновлення номеру телефону для вказаного контакту.'''
        message = "Contact updated."
        name, old_phone, new_phone, *_ = args
        record = book.find(name)
        if record:
            record.edit_phone(old_phone, new_phone)
        else:
            message = f"Contact with name {name} not found!"
        return message

    def show(self, args, book: AddressBook):
        '''Метод повертає телефонні номери для контакту з заданим ім'ям.'''
        return ", ".join(phone.value for phone in book[args[0]].phones)


class BirthdayWorker(BotWorker):
    '''Клас реалізовує оновлення та повернення дня народження для
    вказаного контакту
    '''
    def update(self, args, book: AddressBook):
        '''Метод оновлює дату народження для вказаного контакту.'''
        name, birthday, *_ = args
        record = book.find(name)
        message = "Birthday added."
        if record:
            if record.birthday:
                message = "Birthday updated."
            record.add_birthday(birthday)
        else:
            message = f"Contact with name {name} not found!"
        return message

    def show(self, args, book: AddressBook):
        '''Метод повертає дату народження для вказаного контакту'''
        if book[args[0]].birthday:
            return book[args[0]].birthday.value
        else:
            return f"Birthday for contact with name {args[0]} not found!"
