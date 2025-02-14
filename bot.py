'''Консольний бот помічник, який використовує реалізовані класи для
управління адресною книгою. Реалізовано функціонал для збереження
адресної книги у файл при закритті програми і відновлення при її запуску
'''

import pickle
from contacts import AddressBook, AddressBookValueError
from bot_interface import BotInterface
from workers import ContactWorker, PhonesWorker, BirthdayWorker


class ConsoleBot(BotInterface):
    '''Клас реалізовує консольний бот'''
    def __init__(self):
        self.contact_worker = ContactWorker()
        self.phones_worker = PhonesWorker()
        self.birthday_worker = BirthdayWorker()
        self.book = self.load_data()
        self.args = None

    @staticmethod
    def input_error(func):
        '''Декоратор обробки помилок'''
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except AddressBookValueError as err:
                return str(err)
            except ValueError:
                return "Give me name and phone please."
            except IndexError:
                return "Enter user name."
            except KeyError:
                return "Contact not found!"

        return inner

    @staticmethod
    def parse_input(user_input):
        '''Парсер команд'''
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    @input_error
    def add_contact(self):
        '''Метод додавання нового запису до адресної книги.'''
        return self.contact_worker.update(self.args, self.book)

    @input_error
    def change_contact(self):
        '''Метод збереження нового номеру для контакту із заданим ім'ям.
        Якщо контакт з заданим ім'ям не існує, то користувач отримає
        відповідне повідомлення
        '''
        return self.phones_worker.update(self.args, self.book)

    @input_error
    def show_phone(self):
        '''Метод повертає телефонні номери для контакту з заданим ім'ям.'''
        return self.phones_worker.show(self.args, self.book)

    @input_error
    def add_birthday(self):
        '''Метод додає дату народження для вказаного контакту.'''
        return self.birthday_worker.update(self.args, self.book)

    @input_error
    def show_birthday(self):
        '''Метод повертає дату народження для вказаного контакту'''
        return self.birthday_worker.show(self.args, self.book)

    def show_all(self):
        '''Метод повертає всі записи в адресній книзі'''
        return self.contact_worker.show(self.args, self.book)

    def birthdays(self):
        '''Метод повертає список користувачів, яких потрібно привітати по днях
        на наступному тижні
        '''
        upcoming_birthdays = self.book.get_upcoming_birthdays()
        return f"{'\n'.join(b['name'] + ": " + b['congratulation_date']
                            for b in upcoming_birthdays)}"

    def save_data(self, filename="addressbook.pkl"):
        '''Метод Збереження адресної книги в файл'''
        with open(filename, "wb") as f:
            pickle.dump(self.book, f)

    @staticmethod
    def load_data(filename="addressbook.pkl"):
        '''Метод Відновлення адресної книги з файлу'''
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            # Повернення нової адресної книги, якщо файл не знайдено
            return AddressBook()

    def main(self):
        '''Метод з реалізованою логікою взаємодії з користувачем'''
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            if not user_input or user_input.isspace():
                print("You didn't enter a command.")
                continue

            command, *self.args = self.parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")

            elif command == "add":
                print(self.add_contact())

            elif command == "change":
                print(self.change_contact())

            elif command == "phone":
                print(self.show_phone())

            elif command == "all":
                print(self.show_all())

            elif command == "add-birthday":
                print(self.add_birthday())

            elif command == "show-birthday":
                print(self.show_birthday())

            elif command == "birthdays":
                print(self.birthdays())

            else:
                print("Invalid command.")

        self.save_data(self.book)


if __name__ == "__main__":
    console_bot = ConsoleBot()
    console_bot.main()
