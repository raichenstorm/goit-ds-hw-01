from collections import UserDict
from datetime import datetime, timedelta
from time import strptime
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError
        self.__value = value


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()  # Виправлено формат дати
            super().__init__(value)
        except:
            raise ValueError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if not new_phone.isdigit() or len(new_phone) != 10:
            raise ValueError

        phone_found = False
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                phone_found = True
                break
    
        if not phone_found:
            raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_birthday(self, birthday):
        if isinstance(birthday, Birthday):
            self.birthday = birthday
        else:
            raise ValueError


    def __str__(self):
        phone_numbers = '; '.join(str(p) for p in self.phones)
        birthday_info = f", birthday: {self.birthday.value}" if self.birthday else "-"
        return f"Contact name: {self.name.value}, phones: {phone_numbers}, birthday: {birthday_info}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def save_data(book, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(book, f)

    def load_data(filename="addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except ValueError:
            return "There is no such number in the database"
        
        except KeyError:
            return "There is no such user in the database"
        
        except IndexError:
            return "Index out of range"
    return wrapper


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, *phones = args 
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    for phone in phones: 
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError

@input_error
def show_contact(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return str(record)
    else:
        return "No contacts found"

@input_error
def show_all_contacts(book: AddressBook):
    if book:
        return "\n".join(str(record) for record in book.values())
    else:
        return "No contacts found"
    
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.birthday = Birthday(birthday)
        return "Birthday added successfully"
    else:
        return "No name found"

@input_error
def birthdays(book: AddressBook):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    birthdays_list = []
    for record in book.values():
        if record.birthday:
            if (record.birthday.date.month, record.birthday.date.day) >= (today.month, today.day) and \
               (record.birthday.date.month, record.birthday.date.day) <= (next_week.month, next_week.day):
                birthdays_list.append(str(record))
    if birthdays_list:
        return "\n".join(birthdays_list)
    else:
        return "No upcoming birthdays"

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{record.name.value}'s birthday: {record.birthday}"
    else:
        return f"No birthday information found for {name}"


def main():
    book = AddressBook.load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            book.save_data()
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "show":
            print(show_contact(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))



if __name__ == "__main__":
    main()



