from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio

BOT_TOKEN = "8114296420:AAEu10IU5EE7bcXlsRgaG16LATGELVwxkXM"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_balance = {}


def get_main_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="🪙 Играть в Gem Hunter")
    kb.button(text="💰 Мой баланс")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, persistent=True)


@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_balance:
        user_balance[user_id] = 10000

    await message.answer(
        f"🪙 **Gem Hunter**\n\n"
        f"Баланс: **{user_balance[user_id]:,}** монет",
        reply_markup=get_main_keyboard()
    )


@dp.message(F.text == "🪙 Играть в Gem Hunter")
async def play_game(message: types.Message):
    await message.answer(
        "🎮 Открываем Gem Hunter...",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(
                text="▶️ Запустить игру",
                web_app=types.WebAppInfo(url="https://твой-url.railway.app")  # ← замени после деплоя
            )
        ]])
    )


@dp.message(F.text == "💰 Мой баланс")
async def show_balance(message: types.Message):
    bal = user_balance.get(message.from_user.id, 10000)
    await message.answer(f"💰 Баланс: **{bal:,}** монет", reply_markup=get_main_keyboard())


async def main():
    print("🪙 Gem Hunter запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
