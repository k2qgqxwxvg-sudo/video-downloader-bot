from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import yt_dlp
import os

BOT_TOKEN = "8114296420:AAEu10IU5EE7bcXlsRgaG16LATGELVwxkXM"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

os.makedirs("downloads", exist_ok=True)


def main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🎥 Скачать видео", callback_data="main_menu")
    builder.button(text="🎵 Найти музыку", callback_data="shazam")
    builder.button(text="❤️ Поддержать разработчика", callback_data="donate")
    builder.adjust(1)
    return builder.as_markup()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎥 Бот готов к работе!\n\n"
        "Выбери действие:",
        reply_markup=main_menu()
    )


@dp.message(F.text)
async def download(message: types.Message):
    url = message.text.strip()
    if not url.startswith(("http", "https")):
        return await message.answer("❌ Это не ссылка.")

    wait = await message.answer("⏳ Скачиваю...")

    try:
        ydl_opts = {
            'outtmpl': f'downloads/{message.from_user.id}_%(id)s.%(ext)s',
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as f:
            video_bytes = f.read()

        await message.answer_video(
            types.BufferedInputFile(video_bytes, filename=filename),
            caption=f"✅ Готово!\n{url}"
        )

        os.remove(filename)

    except Exception:
        await wait.edit_text("❌ Не удалось скачать.\nПопробуй другую ссылку.")


# ==================== КНОПКИ ====================

@dp.callback_query(F.data == "main_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎥 Главное меню\nВыбери действие:",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "shazam")
async def shazam_mode(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎵 Отправь мне видео или ссылку — попробую найти трек.\n\n"
        "Для возврата в меню нажми кнопку ниже.",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "donate")
async def donate(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад в меню", callback_data="main_menu")
    
    await callback.message.edit_text(
        "❤️ Спасибо, что хочешь поддержать разработчика!\n\n"
        "Ссылка для доната:\n"
        "https://www.tbank.ru/cf/aTPfX0LC3j",
        reply_markup=builder.as_markup(),
        disable_web_page_preview=True
    )


async def main():
    print("🤖 Бот запущен с удобным меню")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
