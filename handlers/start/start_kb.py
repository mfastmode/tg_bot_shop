from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from core.dictionary import * 

def register_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=register_kb_text, callback_data='register')]
    ])
    return kb

def start_kb():
    kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=start_catalog_text)],
    [KeyboardButton(text=start_order_text)],
    [KeyboardButton(text=start_basket_text)]
    ],
                             resize_keyboard=True,
                             input_field_placeholder='Выберите пункт меню.')

    return kb