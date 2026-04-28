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
    await message.answer(
        "🎥 Бот с cookies (Instagram должен работать лучше).\n"
        "Просто кидай ссылку."
    )


@dp.message(F.text)
async def download(message: types.Message):
    url = message.text.strip()
    if not url.startswith(("http", "https")):
        return await message.answer("❌ Это не ссылка.")

    wait_msg = await message.answer("⏳ Скачиваю с cookies...")

    try:
        ydl_opts = {
            'outtmpl': f'downloads/{message.from_user.id}_%(id)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'cookiefile': 'cookies.txt',          # ← Куки подключены
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            await message.answer_video(
                types.InputFile(video),
                caption=f"✅ Готово!\n{url}"
            )

        os.remove(filename)

    except Exception:
        await wait_msg.edit_text(
            "❌ Не удалось скачать даже с cookies.\n"
            "Попробуй другую ссылку или обнови cookies."
        )


async def main():
    print("🤖 Бот с cookies запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
