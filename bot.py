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


def back_button():
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад в меню", callback_data="back_to_menu")
    return kb.as_markup()


@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🎥 Скачать видео", callback_data="download_mode")
    kb.button(text="🎵 Найти музыку", callback_data="shazam_mode")
    kb.button(text="❤️ Поддержать", callback_data="donate")
    kb.adjust(1)
    
    await message.answer("🎥 Главное меню\nВыбери действие:", reply_markup=kb.as_markup())


# ==================== РЕЖИМЫ ====================

@dp.callback_query(F.data == "download_mode")
async def download_mode(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎥 Отправь ссылку на видео (TikTok, YouTube, Instagram)",
        reply_markup=back_button()
    )


@dp.callback_query(F.data == "shazam_mode")
async def shazam_mode(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎵 Отправь видео, аудио или голосовое сообщение — попробую найти музыку.",
        reply_markup=back_button()
    )


@dp.callback_query(F.data == "donate")
async def donate(callback: types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад в меню", callback_data="back_to_menu")
    await callback.message.edit_text(
        "❤️ Спасибо!\n\nСсылка для поддержки:\nhttps://www.tbank.ru/cf/aTPfX0LC3j",
        reply_markup=kb.as_markup(),
        disable_web_page_preview=True
    )


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="🎥 Скачать видео", callback_data="download_mode")
    kb.button(text="🎵 Найти музыку", callback_data="shazam_mode")
    kb.button(text="❤️ Поддержать", callback_data="donate")
    kb.adjust(1)
    
    await callback.message.edit_text("🎥 Главное меню\nВыбери действие:", reply_markup=kb.as_markup())


# Скачивание видео
@dp.message(F.text)
async def download_video(message: types.Message):
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


# Поиск музыки
@dp.message(F.video | F.audio | F.voice | F.video_note)
async def recognize_music(message: types.Message):
    await message.answer("🎵 Получил файл. Анализирую музыку...")

    # Пока заглушка
    await message.answer(
        "🔍 Пока функция поиска музыки в разработке.\n"
        "Но я уже умею принимать видео и аудио."
    )


async def main():
    print("🤖 Бот с простой навигацией запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
