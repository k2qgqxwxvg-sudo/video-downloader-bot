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
    kb = InlineKeyboardBuilder()
    kb.button(text="🎥 Скачать видео", callback_data="menu")
    kb.button(text="🎵 Найти музыку", callback_data="shazam")
    kb.button(text="❤️ Поддержать", callback_data="donate")
    kb.adjust(1)
    return kb.as_markup()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🎥 Бот готов!\nВыбери действие:", reply_markup=main_menu())


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

@dp.callback_query(F.data == "menu")
async def menu_handler(callback: types.CallbackQuery):
    await callback.message.edit_text("🎥 Отправь ссылку на видео", reply_markup=main_menu())


@dp.callback_query(F.data == "shazam")
async def shazam_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎵 Отправь мне **видео** или **аудиофайл** — попробую определить трек.",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "donate")
async def donate_handler(callback: types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад", callback_data="menu")
    await callback.message.edit_text(
        "❤️ Спасибо!\n\nСсылка для поддержки:\nhttps://www.tbank.ru/cf/aTPfX0LC3j",
        reply_markup=kb.as_markup(),
        disable_web_page_preview=True
    )


# Обработка аудио и видео для поиска музыки
@dp.message(F.voice | F.audio | F.video | F.video_note)
async def recognize_music(message: types.Message):
    await message.answer("🎵 Получил файл. Анализирую музыку... (пока заглушка)")

    # Здесь в будущем можно добавить AudD или Shazam API

    await message.answer(
        "🔍 Пока функция поиска музыки в разработке.\n\n"
        "Но я уже могу принимать аудио и видео."
    )


async def main():
    print("🤖 Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
