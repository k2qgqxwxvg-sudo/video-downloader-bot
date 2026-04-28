from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import os

BOT_TOKEN = "8114296420:AAEu10IU5EE7bcXlsRgaG16LATGELVwxkXM"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Виртуальный баланс
user_balance = {}


def get_main_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🪙 Играть в Gem Hunter", callback_data="play_gemhunter")
    kb.button(text="💰 Мой баланс", callback_data="balance")
    kb.adjust(1)
    return kb.as_markup()


@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_balance:
        user_balance[user_id] = 10000  # стартовые 10.000 монет

    await message.answer(
        f"🪙 Добро пожаловать в **Gem Hunter**!\n\n"
        f"Твой баланс: **{user_balance[user_id]:,}** монет\n\n"
        "Ищи сокровища на поле и избегай бомб!",
        reply_markup=get_main_keyboard()
    )


@dp.callback_query(F.data == "play_gemhunter")
async def play_gemhunter(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🪙 **Gem Hunter** запущен!\n\n"
        "Сейчас откроется игровое поле.",
        reply_markup=None
    )
    
    await callback.message.answer(
        "🎮 Запускаем поле с сокровищами...",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(
                text="▶️ Открыть поле",
                web_app=types.WebAppInfo(url="https://твой-домен.railway.app")  # позже заменим
            )
        ]])
    )


@dp.callback_query(F.data == "balance")
async def show_balance(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    balance = user_balance.get(user_id, 10000)
    await callback.message.edit_text(
        f"💰 Твой баланс:\n\n**{balance:,}** монет",
        reply_markup=get_main_keyboard()
    )


async def main():
    print("🪙 Gem Hunter бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
