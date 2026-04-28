from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import asyncio
import yt_dlp
import os

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "8114296420:AAEu10IU5EE7bcXlsRgaG16LATGELVwxkXM"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Папка для временных файлов
os.makedirs("downloads", exist_ok=True)


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎥 Привет! Отправь мне ссылку на видео из TikTok, YouTube или Instagram — "
        "скачаю без водяных знаков."
    )


@dp.message(F.text)
async def download(message: types.Message):
    url = message.text.strip()
    
    if not url.startswith(("http://", "https://")):
        return await message.answer("❌ Это не ссылка. Отправь правильную ссылку.")

    wait_msg = await message.answer("⏳ Скачиваю видео... Пожалуйста, подожди 10–20 секунд.")

    try:
        ydl_opts = {
            'outtmpl': f'downloads/{message.from_user.id}_%(id)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            },
            # Улучшенные настройки специально для Instagram и TikTok
            'extractor_args': {
                'instagram': {'player_url': True},
                'tiktok': {'webpage': True},
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Отправляем видео
        with open(filename, 'rb') as video:
            await message.answer_video(
                types.InputFile(video),
                caption=f"✅ Готово!\n🔗 {url}"
            )

        # Удаляем файл
        os.remove(filename)

    except Exception:
        await wait_msg.edit_text(
            "❌ Не удалось скачать это видео.\n"
            "Попробуй отправить ссылку ещё раз или другую ссылку."
        )


# ================= ЗАПУСК =================
async def main():
    print("🤖 Бот успешно запущен и работает 24/7")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
