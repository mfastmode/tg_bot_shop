from aiogram import Bot, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from core.dictionary import *
from handlers.start.start_kb import *
from handlers.start.register_state import *
from database.Database import DataBase
import re

start_router = Router()

# Проверка регистрации, если нет то попросит зарегистрироваться
@start_router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    db = DataBase()
    if not await db.get_user(message.from_user.id):
        await bot.send_message(message.from_user.id, register_message, reply_markup=register_kb())
    else:
        await bot.send_message(message.from_user.id, start_message, reply_markup=start_kb())
        
     
@start_router.callback_query(F.data.startswith('register'))
async def start_register(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Для начала укажите ваше имя')
    await state.set_state(RegisterState.name)
    await call.answer()
    
    
@start_router.message(RegisterState.name)
async def username_input(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, 'Укажите ваш номер')
    await state.update_data(name=message.text)
    await state.set_state(RegisterState.phone)
    
    
@start_router.message(RegisterState.phone)
async def register_phone(message: Message, state: FSMContext, bot: Bot):
    if(re.findall('^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', message.text)):
        db = DataBase()
        await state.update_data(phone=message.text)
        reg_data = await state.get_data()
        # Добавление в бд
        await db.add_user(reg_data['name'], reg_data['phone'], message.from_user.id)
        await bot.send_message(message.from_user.id, 'Я вас запомнил!', reply_markup=start_kb())
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, 'Номер указан в неправильном формате')
