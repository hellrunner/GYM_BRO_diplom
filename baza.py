# baza.py

import sqlite3
from cfg import database_name

class SQLutils:
    def __init__(self):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def select_all(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM Users').fetchall()

    def all_info_users(self):
        with self.connection:
            users = self.cursor.execute('SELECT * FROM Users').fetchall()
            info = ''
            num = 0
            for el in users:
                info += f'{el[1]} - {el[2]}\n'
                num += 1
            return info, num
    
    def all_ID_users(self):
        with self.connection:
            users = self.cursor.execute('SELECT * FROM Users').fetchall()
            ID_info = []
            for el in users:
                ID_info.append(el[0])
            return ID_info

    def put_saves_t(self, id, name, save_text):
        with self.connection:
            self.cursor.execute(f'UPDATE Users SET "{name}" = ? WHERE id = ?', (save_text, id))
            self.connection.commit()
    
    def get_saves_t(self, id, save_num):
        with self.connection:
            message_send = self.cursor.execute(f'SELECT "{save_num}" FROM Users WHERE id = ?', (id,)).fetchall()
            try:
                message_send = message_send[0][0]
                if not len(message_send) < 6:
                    return message_send
            except:
                return "Вы еще не сохранили тренировку"
            return "Вы еще не сохранили тренировку"

    def put_favorite_YPR(self, id, save_text):
        with self.connection:
            self.cursor.execute('UPDATE Users SET "favorite_ex" = ? WHERE id = ?', (save_text, id))
            self.connection.commit()
    
    def get_favorite_YPR(self, id):
        with self.connection:
            message_send = self.cursor.execute('SELECT "favorite_ex" FROM Users WHERE id = ?', (id,)).fetchall()
            return message_send[0][0] if message_send else ""

    def count_rows(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM Users').fetchall()
            return len(result)

    def select_single(self, rownum):
        with self.connection:
            return self.cursor.execute('SELECT * FROM Users WHERE id = ?', (rownum,)).fetchall()[0]

    def new_user_add(self, message):
        id = message.from_user.id
        usr_name = "@" + (message.from_user.username or "нету")
        Lname = message.from_user.last_name if message.from_user.last_name else "/none/"
        name = f"{message.from_user.first_name} {Lname}"
        with self.connection:
            try:
                self.cursor.execute('INSERT INTO Users (username, name, id) VALUES (?, ?, ?)', (usr_name, name, id))
                self.connection.commit()
            except:
                pass
            try:
                self.cursor.execute("UPDATE Users SET username = ?, name = ? WHERE id = ?", (usr_name, name, id))
                self.connection.commit()
            except:
                pass

    def close(self):
        self.connection.close()

# === Данные по упражнениям ===

b1gbaza = [
    {"Номер": 1, "Название": "Шраги с гантелями стоя", "Назначение": "Грудь", "Нагрузка": """Нагрузка по 10-ти бальной шкале:
Верх спины	8 (высокая)
Предплечья	4 (средняя)
Нагрузка на позвоночник	5 (средняя)
Общая нагрузка / тип упражнения	
12 (слабая) / изолированное""", "gif_url": "https://i.imgur.com/HuZqKHt.gif", "file_id": " "},
    {"Номер": 2, "Название": "Тяга в наклоне с нижнего блока", "Назначение": "Грудь", "Нагрузка": """Нагрузка по 10-ти бальной шкале:
Широчайшие мышцы  7 (высокая)
Верх спины	7 (высокая)
Задняя дельта  6 (средняя)
Поясница  3 (средняя)
Бицепс  3 (средняя)
Предплечья	3 (средняя)
Нагрузка на позвоночник	2 (слабая) 
Общая нагрузка / тип упражнения
29 (высокая) / базовое глобальное""", "gif_url": "https://i.imgur.com/NW3a7w1.gif", "file_id": " "},
    {"Номер": 3, "Название": "Тяга к груди с верхнего блока широким хватом", "Назначение": "Грудь", "Нагрузка": """Нагрузка по 10-ти бальной шкале:
Широчайшие мышцы  7 (высокая)
Верх спины	7 (высокая)
Бицепс  3 (средняя)
Задняя дельта  3 (средняя)
Предплечья	2 (слабая)
Общая нагрузка / тип упражнения
22 (средняя) / базовое локальное""", "gif_url": "https://i.imgur.com/k4U3sPY.gif", "file_id": " "},
    {"Номер": 4, "Название": "Сгибание рук с гантелями сидя под углом", "Назначение": "Грудь", "Нагрузка": """Нагрузка по 10-ти бальной шкале:
Бицепс	10 (высокая)
Предплечья	2 (слабая)
Общая нагрузка / тип упражнения
12 (слабая) / изолированное""", "gif_url": "https://i.imgur.com/0h5MKNK.gif", "file_id": " "}, 
    {"Номер": 5, "Название": "Тяга гантелей лёжа", "Назначение": "Грудь", "Нагрузка": """Нагрузка по 10-ти бальной шкале:
Широчайшие мышцы  8 (высокая)
Верх спины	5 (средняя)
Задняя дельта  4 (средняя)
Бицепс	4 (средняя)
Предплечья	3 (средняя)
Общая нагрузка / тип упражнения
24 (высокая) / базовое глобальное""", "gif_url": "https://i.imgur.com/iQrHDv7.gif", "file_id": " "},
    {"Номер": 6, "Название": "Тяга горизонтального блока", "Назначение": "Грудь", "Нагрузка": """Нагрузка по 10-ти бальной шкале:
Широчайшие мышцы  10 (высокая)
Верх спины	6 (средняя)
Поясница  3 (средняя)
Задняя дельта  3 (средняя)
Бицепс	3 (средняя)
Предплечья	2 (слабая)
Общая нагрузка / тип упражнения
27 (средняя) / базовое локальное""", "gif_url": "https://i.imgur.com/3pWQxnT.gif", "file_id": " "},
    {"Номер": 7, "Название": "Тяга одной гантели в наклоне", "Назначение": "Грудь", "Нагрузка": """Нагрузка по 10-ти бальной шкале:
Широчайшие мышцы  8 (высокая)
Верх спины	7 (высокая)
Задняя дельта  5 (средняя)
Бицепс	4 (средняя)
Предплечья	3 (средняя)
Общая нагрузка / тип упражнения
27 (высокая) / базовое глобальное""", "gif_url": "https://i.imgur.com/FAZdkcz.gif", "file_id": " "},
    {"Номер": 8, "Название": "Жим штанги лёжа классический", "Назначение": "Грудь", "Нагрузка": """Нагрузка по 10-ти бальной шкале:
Грудь	10 (высокая)
Трицепс	6 (средняя)
Передняя дельта	3 (средняя)
Общая нагрузка / тип упражнения
19 (средняя) / базовое локальное""", "gif_url": "https://i.imgur.com/C5e1VSx.gif", "file_id": " "},
]

count_baza = {
    "Шраги с гантелями стоя": 1,
    "Тяга в наклоне с нижнего блока": 2,
    "Тяга к груди с верхнего блока широким хватом": 3,
    "Сгибание рук с гантелями сидя под углом": 4,
    "Тяга гантелей лёжа": 5,
    "Тяга горизонтального блока": 6,
    "Тяга одной гантели в наклоне": 7,
    "Жим штанги лёжа классический": 8
}

group_baza = {
    "Грудь": "8",
    "Спину": "1,2,3,5,6,7",
    "Руки": "4",
    "Ноги": "",
    "Плечи": ""
}

group = ["Грудь", "Спину", "Руки", "Ноги", "Плечи"]

# ===================== Вспомогательные функции вывода ====================

def print_all_baza():
    mess = ""
    for muscle in group:
        x = group_baza[muscle].split(",")
        mess += f"Упражнения на {muscle}:\n"
        for num in count_baza:
            if str(count_baza[num]) in x:
                mess += f"{count_baza[num]}. {num}\n"
        mess += "\n"
    return f'Список всех упражнений.\n{mess}'

def print_full_baza():
    mess = ""
    for muscle in group:
        x = group_baza[muscle].split(",")
        mess += f"Упражнения на {muscle}.\n"
        for num in count_baza:
            if str(count_baza[num]) in x:
                y = count_baza[num] - 1
                mess += f'{b1gbaza[y]["Номер"]}. {b1gbaza[y]["Название"]}\n'
        mess += "\n"
    return f'Список всех упражнений:\n{mess}'

def print_group(text):
    mess = ""
    x = group_baza[text].split(",")
    for i in count_baza:
        if str(count_baza[i]) in x:
            mess += f"{count_baza[i]}) {i}\n"
    return f'Список упражнений на {text}:\n{mess}'

def print_all_by_nums(mass):
    mess = ""
    try:
        for el in mass:
            for C in count_baza:
                if int(el) == count_baza[C]:
                    mess += f"{count_baza[C]}. {C}\n"
        return mess
    except:
        return None

def print_all_by_nums_NO_MESSAGE(mass):
    mess = ""
    for el in mass:
        for C in count_baza:
            if int(el) == count_baza[C]:
                mess += f"{count_baza[C]}. {C}\n"
    return mess

def print_by_num_from_b1gbaza(num):
    mess = 'ошибка'
    if num != "нету":
        for C in count_baza:
            if num == count_baza[C]:
                num = num - 1
                mess = f'{b1gbaza[num]["Номер"]}. {b1gbaza[num]["Название"]}\n{b1gbaza[num]["Нагрузка"]}'
    else:
        mess = "Нет сохраненных упражнений"
    if mess == "ошибка":
        mess = f"На данный момент нет упражнения под номером {num}"
    return mess
