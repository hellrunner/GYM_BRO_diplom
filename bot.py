import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

from cfg import token, admin_users, help_text
import funcs_markup
import baza
from callbacks import router as callbacks_router

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(callbacks_router)  # регистрация всех inline-колбеков

users_online_bot = []

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    markup = funcs_markup.get_start_keyboard()
    if message.from_user.id not in users_online_bot:
        db = baza.SQLutils()
        db.new_user_add(message)
        db.close()
        users_online_bot.append(message.from_user.id)
    await message.answer(
        f"Бот готов служить, {message.from_user.first_name}.\nПолучить справку: /help",
        reply_markup=markup
    )

@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(help_text)

# ====== Reply-кнопки ======

@dp.message(F.text == "gym")
async def gym_menu(message: types.Message):
    markup = funcs_markup.get_gym_keyboard()
    await message.answer("Меню тренажёрного зала", reply_markup=markup)

@dp.message(F.text == "Мои тренировки")
async def my_trains(message: types.Message):
    photo = "AgACAgIAAxkBAAIydGhBobEFjgYfIRDFKf5lRWh6l-t4AAKF9DEbJH4QSlmiEWoVFE9rAQADAgADeQADNgQ"
    markup = funcs_markup.get_gym_my_trains_keyboard()
    await message.answer_photo(photo=photo, caption="Ваши тренировки:", reply_markup=markup)

@dp.message(F.text == "База упражнений")
async def baza_menu(message: types.Message):
    markup = funcs_markup.get_baza_keyboard()
    await message.answer("Меню базы упражнений", reply_markup=markup)

@dp.message(F.text == "Вывести все упражнения")
async def show_all_exercises(message: types.Message):
    await message.answer(baza.print_all_baza())

@dp.message(F.text == "Группы мышц")
async def muscle_groups(message: types.Message):
    markup = funcs_markup.get_gym_group_keyboard()
    await message.answer("Выберите группу мышц:", reply_markup=markup)

@dp.message(F.text.in_(baza.group))
async def group_exercises(message: types.Message):
    await message.answer(baza.print_group(message.text))

@dp.message(F.text == "Избранное")
async def show_favorites(message: types.Message):
    await message.answer(f"Ваше избранное:\n{funcs_markup.favorite_show(message.from_user.id)}")

@dp.message(F.text == "я admin")
async def admin_menu(message: types.Message):
    if message.from_user.id in admin_users:
        markup = funcs_markup.get_admin_keyboard()
        await message.answer("Привет, хозяин", reply_markup=markup)
    else:
        await message.answer("К сожалению, вы не админ.")
# Вернуться в стартовое меню
@dp.message(F.text == "Вернуться")
async def return_start(message: types.Message):
    markup = funcs_markup.get_start_keyboard()
    await message.answer("Вы в главном меню", reply_markup=markup)

# Вернуться в меню тренажерного зала (gym)
@dp.message(F.text == "вернуться в gym")
async def return_gym(message: types.Message):
    markup = funcs_markup.get_gym_keyboard()
    await message.answer("Меню тренажёрного зала", reply_markup=markup)

# Вернуться в меню базы упражнений
@dp.message(F.text == "вернуться в базу")
async def return_baza(message: types.Message):
    markup = funcs_markup.get_baza_keyboard()
    await message.answer("Меню базы упражнений", reply_markup=markup)


# ===== Любой другой текст =====
@dp.message()
async def unknown_message(message: types.Message):
    await message.answer("Не понимаю, воспользуйтесь меню или /help.")

# =========== Запуск ===========
if __name__ == "__main__":
    print("Бот запущен!")
    asyncio.run(dp.start_polling(bot))
