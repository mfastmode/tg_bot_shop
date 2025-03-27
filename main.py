from aiogram import Dispatcher, Bot, F
import asyncio
import os
from dotenv import load_dotenv
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from database.Database import DataBase


load_dotenv()

token = os.getenv("TOKEN_ID")
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Прописываем свой телеграм id чтобы бот прислал сообщение
async def start_bot(bot: Bot):
    await bot.send_message(chat_id=1931071564, text='Я запустил бота')
    
    
dp.startup.register(start_bot)


async def start():
    try:
        # Создание базы
        db = DataBase()
        await db.create_db()
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
        

if __name__ == "__main__":
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Exit')