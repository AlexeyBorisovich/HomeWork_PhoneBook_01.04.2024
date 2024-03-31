'''
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной
'''

from os.path import exists
from csv import DictReader, DictWriter

import os
from os.path import exists
from csv import DictWriter, DictReader


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_info():
    is_valid_first_name = False
    while not is_valid_first_name:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Не валидное имя")
            else:
                is_valid_first_name = True
        except NameError as err:
            print(err)
            continue

    is_valid_last_name = False
    while not is_valid_last_name:
        try:
            last_name = input("Введите фамилию: ")
            if len(last_name) < 2:
                raise NameError("Не валидная фамилия")
            else:
                is_valid_last_name = True
        except NameError as err:
            print(err)
            continue

    is_valid_phone = False
    while not is_valid_phone:
        try:
            phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Неверная длина номера")
            else:
                is_valid_phone = True
        except ValueError:
            print("Не валидный номер!!!")
            continue
        except LenNumberError as err:
            print(err)
            continue

    return [first_name, last_name, phone_number]


def create_file(file_name):
    with open(file_name, "w", encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()


def read_file(file_name):
    with open(file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name, lst):
    res = read_file(file_name)
    for el in res:
        if el["Телефон"] == str(lst[2]):
            print("Такой телефон уже есть")
            return

    obj = {"Имя": lst[0], "Фамилия": lst[1], "Телефон": lst[2]}
    res.append(obj)
    with open(file_name, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)


def rou_search(file_name):
    last_name = input("Введите фамилию для поиска: ")
    res = read_file(file_name)
    for elem in res:
        if elem["Фамилия"] == last_name:
            print(elem)
            break
    else:
        print("Фамилии нет")


def copy_entry(source_file, row_number):
    # Получаем текущую рабочую папку
    current_dir = os.getcwd()
    target_file = os.path.join(current_dir, "phone_copy.csv")  # Создаем путь к новому файлу в текущей папке

    source_data = read_file(source_file)
    if row_number <= len(source_data):
        entry_to_copy = source_data[row_number - 1]  # Adjusting for 0-based index
        create_file(target_file)  # Создаем новый файл с такими же параметрами
        # Записываем выбранную запись из исходного файла в новый файл
        with open(target_file, "a", encoding='utf-8', newline='') as data:
            f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
            f_writer.writerow(
                {'Имя': entry_to_copy['Имя'], 'Фамилия': entry_to_copy['Фамилия'], 'Телефон': entry_to_copy['Телефон']})
    else:
        print("Неверный номер строки!")


def main():
    file_name = 'phone.csv'
    while True:
        command = input("Введите команду: ")
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, get_info())
        elif command == 'r':
            if not exists(file_name):
                print("Файл отсутствует. Создайте его")
                continue
            print(*read_file(file_name))
        elif command == 'f':
            if not exists(file_name):
                print("Файл отсутствует. Создайте его")
                continue
            rou_search(file_name)
        elif command == 'c':
            if not exists(file_name):
                print("Исходный файл отсутствует. Создайте его")
                continue
            row_number = int(input("Введите номер строки для копирования: "))
            copy_entry(file_name, row_number)


main()

