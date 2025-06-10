# callbacks.py

from aiogram import Router, types, F
from aiogram.types import CallbackQuery, InputMediaPhoto, InputMediaAnimation
import funcs_markup
import baza
from cfg import admin_users

router = Router()

# === Хранение временных данных, как и раньше ===
users_id_show_more_saves = []
save_read = []
save_read_users = []
maybe = ""

# --- Колбеки для редактирования тренировок ---
@router.callback_query(F.data == "edit_saves")
async def callback_edit_saves(call: CallbackQuery):
    markup = funcs_markup.get_gym_new_train_keyboard()
    await call.message.answer(
        "Выберете какую тренировку хотите создать\\изменить. Ниже указаны номера сохранений, вывести все упражнения либо избранные или по группе мышц.",
        reply_markup=markup
    )
    await call.answer()

# --- Колбеки для сохранения тренировок ---
for i in range(1, 6):
    @router.callback_query(F.data == f"save_train_{i}")
    async def callback_save_train(call: CallbackQuery, num=i):
        await call.message.answer("Введите номера упражнений через запятую.\nПример: 1,2,3,4,5")
        # В aiogram нет register_next_step_handler, обычно юзают FSM, но можно сделать просто жёстко: 
        # на следующем сообщении пользователя ловить ответ вручную (или реализовать FSM позже)
        # Пока этот функционал добавим в основном файле с использованием aiogram FSM
        await call.answer()

# --- Колбеки для вывода всех упражнений и по группам ---
@router.callback_query(F.data == "save_show_all_YPR")
async def callback_save_show_all_YPR(call: CallbackQuery):
    text = baza.print_all_baza()
    await call.message.answer(text)
    await call.answer()

@router.callback_query(F.data == "save_show_fav_YPR")
async def callback_save_show_fav_YPR(call: CallbackQuery):
    text = funcs_markup.favorite_show(call.from_user.id)
    await call.message.answer(f"Ваше избранное:\n{text}")
    await call.answer()

@router.callback_query(F.data == "save_show_legs")
async def callback_show_group_legs(call: CallbackQuery):
    await call.message.answer(baza.print_group("Ноги"))
    await call.answer()

@router.callback_query(F.data == "save_show_back")
async def callback_show_group_back(call: CallbackQuery):
    await call.message.answer(baza.print_group("Спину"))
    await call.answer()

@router.callback_query(F.data == "save_show_arms")
async def callback_show_group_arms(call: CallbackQuery):
    await call.message.answer(baza.print_group("Руки"))
    await call.answer()

@router.callback_query(F.data == "save_show_chest")
async def callback_show_group_chest(call: CallbackQuery):
    await call.message.answer(baza.print_group("Грудь"))
    await call.answer()

@router.callback_query(F.data == "save_show_shoulders")
async def callback_show_group_shoulders(call: CallbackQuery):
    await call.message.answer(baza.print_group("Плечи"))
    await call.answer()

# --- Мои тренировки/Подробнее/Редактировать ---
@router.callback_query(F.data == "show_my_trains")
async def callback_show_my_trains(call: CallbackQuery):
    photo = "AgACAgIAAxkBAAIydGhBobEFjgYfIRDFKf5lRWh6l-t4AAKF9DEbJH4QSlmiEWoVFE9rAQADAgADeQADNgQ"
    markup = funcs_markup.get_gym_my_trains_keyboard()
    await call.message.answer_photo(photo=photo, caption="Ваши тренировки:", reply_markup=markup)
    await call.answer()

@router.callback_query(F.data == "more_info_saves")
async def callback_more_info(call: CallbackQuery):
    users_id_show_more_saves.append(call.from_user.id)
    markup = funcs_markup.get_gym_my_trains_deep_keyboard()
    await call.message.edit_reply_markup(reply_markup=markup)
    await call.answer()

@router.callback_query(F.data == "less_info_saves")
async def callback_less_info(call: CallbackQuery):
    try:
        users_id_show_more_saves.remove(call.from_user.id)
    except:
        pass
    markup = funcs_markup.get_gym_my_trains_keyboard()
    await call.message.edit_reply_markup(reply_markup=markup)
    await call.answer()

# --- Админские кнопки: рассылка ---
@router.callback_query(F.data == "send_all_yes")
async def callback_send_all_yes(call: CallbackQuery):
    # Здесь должен быть текст рассылки, его лучше хранить в user state/FSM
    await call.message.answer("Рассылка всем пользователям пока не реализована.")
    await call.answer()

@router.callback_query(F.data == "send_all_no")
async def callback_send_all_no(call: CallbackQuery):
    await call.message.answer("Вы ничего не отправили")
    await call.answer()

# --- Тренировки (кнопки 1-5) ---
@router.callback_query(F.data.in_({"save1", "save2", "save3", "save4", "save5"}))
async def callback_train_page(call: CallbackQuery):
    train_number = int(call.data.replace("save", ""))
    db = baza.SQLutils()
    text = db.get_saves_t(call.from_user.id, f"my_train_{train_number}")
    db.close()
    if not text or text == "Вы еще не сохранили тренировку":
        caption = "Ваша тренировка:\nВы еще не сохранили тренировку"
    else:
        # Можно красиво выводить упражнения через baza.print_all_by_nums
        caption = f"Ваша тренировка:\n{text}"
    markup = funcs_markup.get_gym_my_trains_keyboard()
    # пытаемся редактировать caption (если есть фото), иначе просто text
    try:
        await call.message.edit_caption(caption=caption, reply_markup=markup)
    except Exception:
        await call.message.edit_text(text=caption, reply_markup=markup)
    await call.answer()

