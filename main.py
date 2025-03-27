from aiogram import Dispatcher, Bot, F
import asyncio
import os
from dotenv import load_dotenv
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from handlers.start.start import start_router


load_dotenv()

token = os.getenv("TOKEN_ID")
my_tg_id = os.getenv("TG_ID")
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Прописываем свой телеграм id чтобы бот прислал сообщение
async def start_bot(bot: Bot):
    await bot.send_message(chat_id=my_tg_id, text='Я запустил бота')
    
    
dp.startup.register(start_bot)
dp.include_routers(start_router)

async def start():
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
        

if __name__ == "__main__":
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Exit')