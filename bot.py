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
    await message.answer("🎥 Привет! Просто отправь мне ссылку на видео из TikTok, YouTube или Instagram — скачаю без водяных знаков.")

@dp.message(F.text)
async def download(message: types.Message):
    url = message.text.strip()
    if not url.startswith(("http://", "https://")):
        return await message.answer("❌ Это не ссылка")

    msg = await message.answer("⏳ Скачиваю видео...")

    try:
               ydl_opts = {
            'outtmpl': f'downloads/{message.from_user.id}_%(id)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            # Дополнительные настройки специально для Instagram и TikTok
            'extractor_args': {
                'instagram': {
                    'player_url': True,
                },
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await message.answer_video(
            types.InputFile(filename),
            caption=f"✅ Готово!\n🔗 {url}"
        )

        os.remove(filename)  # удаляем файл после отправки

    except Exception as e:
        await msg.edit_text(f"❌ Не удалось скачать.\nПопробуй другую ссылку.")

async def main():
    print("🤖 Бот запущен и работает 24/7")
    await dp.start_polling(bot)

if __name__ == "__main__":      # ← Правильно так
    asyncio.run(main())
