from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from pytube import YouTube
import os
import requests

from keep_alive import keep_alive

keep_alive()




# @willnes_bot
API_TOKEN = '7558561191:AAE4KBjYYpL3lgGAccRI-TY9OLesCQFRdbM'  # BotFatherdan olingan tokenni qo'ying

# Bot va Dispatcher obyektlari
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# YouTube video yuklash funksiyasi
def download_video(url, is_short=False):
    try:
        yt = YouTube(url)
        if is_short:
            stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
        else:
            stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
        video_path = stream.download(output_path='downloads')
        return video_path
    except Exception as e:
        print(f"Xato: {e}")
        return None

# /start komandasi
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu alaykum! YouTube video yuklash botiga xush kelibsiz. Video yuklash uchun video linkini yuboring.")

# Video linkini qabul qilish
@dp.message_handler(lambda message: message.text.startswith('https://www.youtube.com/') or message.text.startswith('https://youtu.be/'))
async def handle_video_link(message: types.Message):
    url = message.text
    is_short = 'shorts' in url  # YouTube Shorts ekanligini tekshirish

    await message.reply("Video yuklanmoqda...")

    # Videoni yuklash
    video_path = download_video(url, is_short)
    if video_path:
        await message.reply("Video yuklandi. Yuborilmoqda...")
        with open(video_path, 'rb') as video_file:
            await message.reply_video(video_file, caption="YouTube videosi")
        os.remove(video_path)  # Faylni o'chirish
    else:
        await message.reply("Xato: Video yuklanmadi. Iltimos, havolani tekshiring.")

# Botni ishga tushirish
if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    executor.start_polling(dp, skip_updates=True)