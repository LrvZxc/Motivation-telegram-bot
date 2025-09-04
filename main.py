import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os
from dotenv import load_dotenv
print("🚀 Бот запущен с новой версией кода!")
load_dotenv()

TOKEN = os.getenv("Token") 



dp = Dispatcher()
RU = False
EN = False

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    global RU, EN
    print(f"Пользователь {message.from_user.full_name} запустил бота.")
    
    keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Русский"),
            KeyboardButton(text="English"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
    
    await message.answer(f"""Ну привет, {html.bold(message.from_user.full_name)}. Я бот который может тебя мотивировать\
                        напиши /quote и я залью мотивации\n
                        Для начала, напиши язык на котором ты хочешь видеть цитаты""", reply_markup=keyboard) 
    while RU == False and EN == False:
        await message.answer("Выбери язык", reply_markup=keyboard)
    user_lang = {}
    if message.text == "Русский":
      
        user_lang[message.from_user.id] = "RU"
        
        await message.answer("Отлично! Теперь ты будешь получать цитаты на русском языке. Напиши /quote чтобы получить первую цитату.")
    elif message.text == "English":

        user_lang = {}
        user_lang[message.from_user.id] = "EN"
      
        await message.answer("Great! Now you will receive quotes in English. Type /quote to get your first quote.")
@dp.message(Command("quote"))
async def quote(message: Message) -> None:
    global RU, EN
    if EN:
        file_path = "C:\\Users\\marat\\OneDrive\\Рабочий стол\\тгБот\\Motivation-telegram-bot\\Quotes.txt"
    elif RU:
        file_path = "C:\\Users\\marat\\OneDrive\\Рабочий стол\\тгБот\\Motivation-telegram-bot\\RuQuotes.txt"
    
        with open(file_path, "r", encoding="utf-8") as file:
            import random
            quotes = [line.strip() for line in file if line.strip()]
            temp = random.choice(quotes)
            print(type(temp), temp)
            if isinstance(temp, str) and " — " in temp:
                quotea, author = temp.rsplit(" — ", 1)
                await message.answer(f"💬{quotea.strip()}\n- 👤{author.strip()}")
            elif isinstance(temp, str):
                await message.answer(temp)
   
        
async def main() -> None:

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
 

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())