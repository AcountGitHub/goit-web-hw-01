'''Консольний бот помічник, який використовує реалізовані класи для
управління адресною книгою. Реалізовано функціонал для збереження
адресної книги у файл при закритті програми і відновлення при її запуску
'''

from contacts import AddressBookValueError
from bot_interface import BotInterface
from workers import ContactWorker, PhonesWorker, BirthdayWorker, PickleWorker


class ConsoleBot(BotInterface):
    '''Клас реалізовує консольний бот'''
    def __init__(self):
        self.pickle_worker = PickleWorker()
        self.contact_worker = None
        self.phones_worker = None
        self.birthday_worker = None
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
        return self.contact_worker.update(self.args)

    @input_error
    def change_contact(self):
        '''Метод збереження нового номеру для контакту із заданим ім'ям.
        Якщо контакт з заданим ім'ям не існує, то користувач отримає
        відповідне повідомлення
        '''
        return self.phones_worker.update(self.args)

    @input_error
    def show_phone(self):
        '''Метод повертає телефонні номери для контакту з заданим ім'ям.'''
        return self.phones_worker.show(self.args)

    @input_error
    def add_birthday(self):
        '''Метод додає дату народження для вказаного контакту.'''
        return self.birthday_worker.update(self.args)

    @input_error
    def show_birthday(self):
        '''Метод повертає дату народження для вказаного контакту'''
        return self.birthday_worker.show(self.args)

    def show_all(self):
        '''Метод повертає всі записи в адресній книзі'''
        return self.contact_worker.show()

    def birthdays(self):
        '''Метод повертає список контактів, яких потрібно привітати по днях
        на наступному тижні
        '''
        return self.birthday_worker.show_upcoming_birthdays()

    def main(self):
        '''Метод з реалізованою логікою взаємодії з користувачем'''
        book = self.pickle_worker.load_data("contacts.dat")
        self.contact_worker = ContactWorker(book)
        self.phones_worker = PhonesWorker(book)
        self.birthday_worker = BirthdayWorker(book)
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

        self.pickle_worker.save_data(book, "contacts.dat")


if __name__ == "__main__":
    console_bot = ConsoleBot()
    console_bot.main()
