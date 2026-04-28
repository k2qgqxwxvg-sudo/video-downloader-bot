from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import asyncio
import yt_dlp
import os

BOT_TOKEN = "8114296420:AAEu10IU5EE7bcXlsRgaG16LATGELVwxkXM"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

os.makedirs("downloads", exist_ok=True)


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🎥 Бот исправлен.\nКидай ссылку на TikTok или YouTube.")


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

        # Правильный способ отправки видео в aiogram 3
        with open(filename, 'rb') as f:
            video_bytes = f.read()

        await message.answer_video(
            types.BufferedInputFile(video_bytes, filename=filename),
            caption=f"✅ Готово!\n{url}"
        )

        os.remove(filename)

    except Exception as e:
        await wait.edit_text(f"❌ Ошибка: {str(e)[:150]}...\nПопробуй другую ссылку.")


async def main():
    print("🤖 Бот запущен (исправленная версия)")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
