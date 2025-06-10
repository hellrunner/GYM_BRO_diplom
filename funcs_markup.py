# funcs_markup.py

from aiogram import types
import baza

# ============ Reply-клавиатуры ============

def get_start_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="gym"), types.KeyboardButton(text="🛠️")],
            [types.KeyboardButton(text="я admin")]
        ],
        resize_keyboard=True
    )

def get_gym_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Мои тренировки"), types.KeyboardButton(text="База упражнений"), types.KeyboardButton(text="🛠️")],
            [types.KeyboardButton(text="Вернуться")]
        ],
        resize_keyboard=True
    )

def get_baza_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Вывести все упражнения"), types.KeyboardButton(text="Группы мышц"), types.KeyboardButton(text="Избранное")],
            [types.KeyboardButton(text="вернуться в gym")]
        ],
        resize_keyboard=True
    )

def get_gym_group_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Спину"), types.KeyboardButton(text="Грудь"), types.KeyboardButton(text="Ноги"), types.KeyboardButton(text="Руки"), types.KeyboardButton(text="Плечи")],
            [types.KeyboardButton(text="вернуться в базу")]
        ],
        resize_keyboard=True
    )

def get_admin_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Все пользователи"), types.KeyboardButton(text="Отправить всем")],
            [types.KeyboardButton(text="Вернуться")]
        ],
        resize_keyboard=True
    )

# ============ Inline-клавиатуры ============

def get_gym_my_trains_keyboard():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="1", callback_data="save1"),
            types.InlineKeyboardButton(text="2", callback_data="save2"),
            types.InlineKeyboardButton(text="3", callback_data="save3"),
            types.InlineKeyboardButton(text="4", callback_data="save4"),
            types.InlineKeyboardButton(text="5", callback_data="save5"),
        ],
        [
            types.InlineKeyboardButton(text="Подробнее", callback_data="more_info_saves"),
            types.InlineKeyboardButton(text="Редактировать", callback_data="edit_saves"),
        ]
    ])
    return markup

def get_gym_my_trains_deep_keyboard():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="<-", callback_data="<-"),
            types.InlineKeyboardButton(text="->", callback_data="->"),
        ],
        [
            types.InlineKeyboardButton(text="1", callback_data="save1"),
            types.InlineKeyboardButton(text="2", callback_data="save2"),
            types.InlineKeyboardButton(text="3", callback_data="save3"),
            types.InlineKeyboardButton(text="4", callback_data="save4"),
            types.InlineKeyboardButton(text="5", callback_data="save5"),
        ],
        [
            types.InlineKeyboardButton(text="Убрать подробности", callback_data="less_info_saves"),
            types.InlineKeyboardButton(text="Редактировать", callback_data="edit_saves"),
        ]
    ])
    return markup

def get_gym_new_train_keyboard():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="1", callback_data="save_train_1"),
            types.InlineKeyboardButton(text="2", callback_data="save_train_2"),
            types.InlineKeyboardButton(text="3", callback_data="save_train_3"),
            types.InlineKeyboardButton(text="4", callback_data="save_train_4"),
            types.InlineKeyboardButton(text="5", callback_data="save_train_5"),
        ],
        [
            types.InlineKeyboardButton(text="все упр", callback_data="save_show_all_YPR"),
            types.InlineKeyboardButton(text="Избранное", callback_data="save_show_fav_YPR"),
        ],
        [
            types.InlineKeyboardButton(text="Ноги", callback_data="save_show_legs"),
            types.InlineKeyboardButton(text="Спину", callback_data="save_show_back"),
            types.InlineKeyboardButton(text="Руки", callback_data="save_show_arms"),
            types.InlineKeyboardButton(text="Грудь", callback_data="save_show_chest"),
            types.InlineKeyboardButton(text="Плечи", callback_data="save_show_shoulders"),
        ]
    ])
    return markup

# ========== Функции работы с избранным, сохранением и выводом ==========

def save_train1_5(user_id, text, number):
    db = baza.SQLutils()
    save_ypr = "       " + text
    db.put_saves_t(user_id, f"my_train_{number}", save_ypr)
    db.close()
    return baza.print_all_by_nums(text.split(","))

def add_favorite_todb(user_id, text):
    db = baza.SQLutils()
    fav_mess = baza.print_all_by_nums(text.split(","))
    old_mess = db.get_favorite_YPR(user_id)
    if old_mess is None:
        old_mess = ""
    new_fav = old_mess + fav_mess
    db.put_favorite_YPR(user_id, new_fav)
    db.close()
    return fav_mess

def del_by_num(user_id, text):
    end_save = ""
    end_mess = ""
    nums = text.split(",")
    db = baza.SQLutils()
    massiv = db.get_favorite_YPR(user_id).split('\n')
    for num in nums:
        del_num = str(int(num)) + "."
        for el in range(len(massiv) - 1):
            if del_num in massiv[el]:
                end_mess += f"{massiv[el]}\n"
                massiv.pop(el)
                break
    for strochka in massiv:
        if strochka != "":
            end_save += f"{strochka}\n"
    db.put_favorite_YPR(user_id, end_save)
    db.close()
    return end_mess

def favorite_show(user_id):
    db = baza.SQLutils()
    fav = db.get_favorite_YPR(user_id)
    db.close()
    return fav if fav else "У вас пока нет избранных упражнений."
