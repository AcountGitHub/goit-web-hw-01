'''Абстрактний клас із методами для реалізації ботом помічником'''

from abc import ABC, abstractmethod

class BotInterface(ABC):
    '''Абстрактний клас, який є загальним інтерфейсом бота'''

    @abstractmethod
    def add_contact(self):
        '''Абстрактний метод додавання нового контакту'''
        pass

    @abstractmethod
    def change_contact(self):
        '''Абстрактний метод збереження нового номеру для контакту'''
        pass

    @abstractmethod
    def show_phone(self):
        '''Абстрактний метод поверненя телефонних номерів для контакту
        з заданим ім'ям.
        '''
        pass

    @abstractmethod
    def add_birthday(self):
        '''Абстрактний метод додавання дати народження для вказаного контакту.'''
        pass

    @abstractmethod
    def show_birthday(self):
        '''Абстрактний метод повернення дати народження для вказаного контакту.'''
        pass

    @abstractmethod
    def show_all(self):
        '''Абстрактний метод повернення всіх записів в адресній книзі'''
        pass
