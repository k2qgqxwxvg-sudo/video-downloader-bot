from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio
import yt_dlp
import os

BOT_TOKEN = "8114296420:AAEu10IU5EE7bcXlsRgaG16LATGELVwxkXM"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

os.makedirs("downloads", exist_ok=True)


def get_main_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="🎥 Скачать видео")
    kb.button(text="🎵 Найти музыку")
    kb.button(text="❤️ Поддержать разработчика")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, persistent=True)


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎥 Бот готов к работе!\n\n"
        "Используй кнопки внизу:",
        reply_markup=get_main_keyboard()
    )


# ==================== МЕНЮ ====================

@dp.message(F.text == "🎥 Скачать видео")
async def download_mode(message: types.Message):
    await message.answer("🎥 Отправь ссылку на видео из TikTok, YouTube или Instagram.")


@dp.message(F.text == "🎵 Найти музыку")
async def music_mode(message: types.Message):
    await message.answer("🎵 Отправь видео, аудио или голосовое сообщение — попробую найти трек.")


@dp.message(F.text == "❤️ Поддержать разработчика")
async def donate(message: types.Message):
    await message.answer(
        "❤️ Спасибо за поддержку!\n\n"
        "Ссылка для доната:\n"
        "https://www.tbank.ru/cf/aTPfX0LC3j"
    )


# ==================== СКАЧИВАНИЕ ====================
@dp.message(F.text)
async def download_video(message: types.Message):
    url = message.text.strip()
    if not url.startswith(("http", "https")):
        return  # Игнорируем обычные сообщения

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


# ==================== ПОИСК МУЗЫКИ ====================
@dp.message(F.video | F.audio | F.voice | F.video_note)
async def recognize_music(message: types.Message):
    await message.answer("🎵 Анализирую музыку...")


async def main():
    print("🤖 Бот с нижним меню запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
