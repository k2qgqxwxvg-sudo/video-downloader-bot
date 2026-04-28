from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import yt_dlp
import os
import requests
import base64

BOT_TOKEN = "8114296420:AAEu10IU5EE7bcXlsRgaG16LATGELVwxkXM"

# ACRCloud данные
ACR_HOST = "identify-ap-southeast-1.acrcloud.com"
ACR_ACCESS_KEY = "158dc59075112f298d5990c9b64478c7"
ACR_ACCESS_SECRET = "UHbjn3ORI73axkO80oJO5trn4iIHaSTiNdvQxmmP"

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


# ==================== СКАЧИВАНИЕ ====================
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
        await wait.edit_text("❌ Не удалось скачать.")


# ==================== ПОИСК МУЗЫКИ ====================
@dp.message(F.video | F.audio | F.voice | F.video_note)
async def recognize_music(message: types.Message):
    await message.answer("🎵 Анализирую музыку...")

    file = await message.bot.download(message.video or message.audio or message.voice or message.video_note)
    file_bytes = file.read()

    # Отправляем на ACRCloud
    try:
        response = requests.post(
            f"https://{ACR_HOST}/v1/identify",
            files={"sample": file_bytes},
            data={
                "access_key": ACR_ACCESS_KEY,
                "access_secret": ACR_ACCESS_SECRET,
                "data_type": "audio",
                "signature_version": "1",
            },
            timeout=15
        )

        result = response.json()

        if result.get("status", {}).get("code") == 0:
            music = result["metadata"]["music"][0]
            title = music["title"]
            artist = music["artists"][0]["name"]
            album = music.get("album", {}).get("name", "Неизвестно")

            await message.answer(
                f"✅ Трек найден!\n\n"
                f"🎵 Название: {title}\n"
                f"👤 Исполнитель: {artist}\n"
                f"💿 Альбом: {album}"
            )
        else:
            await message.answer("❌ Не удалось определить трек. Попробуй другое видео.")

    except Exception:
        await message.answer("❌ Ошибка при распознавании музыки.")


# ==================== КНОПКИ ====================

@dp.callback_query(F.data == "menu")
async def menu_handler(callback: types.CallbackQuery):
    await callback.message.edit_text("🎥 Отправь ссылку на видео", reply_markup=main_menu())


@dp.callback_query(F.data == "shazam")
async def shazam_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎵 Отправь видео, аудио или голосовое — попробую найти трек.",
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


async def main():
    print("🤖 Бот с реальным распознаванием музыки запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
