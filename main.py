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


user_lang = {}
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
   
    print(f"Пользователь {message.from_user.id} запустил бота.")
    
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
    
    await message.answer(f"""Ну привет, {html.bold(message.from_user.full_name)}. Я бот который может тебя мотивировать\n
                        напиши /quote и я залью мотивации\n
                        Для начала, напиши язык на котором ты хочешь видеть цитаты""", reply_markup=keyboard) 
    
@dp.message(lambda message: message.text in ["Русский", "English"])
async def language_selection(message: Message) -> None:
    selected_language = message.text
    if selected_language == "Русский":
        await message.answer("Отлично! Теперь ты будешь получать цитаты на русском языке. Напиши /quote чтобы получить цитату.")
        user_lang[message.from_user.id] = "RU"
    elif selected_language == "English":
        user_lang[message.from_user.id] = "EN"
        await message.answer("Great! Now you will receive quotes in English. Type /quote to get a quote.")
    print(f"Пользователь {message.from_user.full_name} с айди {message.from_user.id} выбрал язык {selected_language}.")

@dp.message(Command("quote"))
async def quote(message: Message) -> None:
    print(f"Пользователь {message.from_user.full_name} с айди {message.from_user.id} запросил цитату.")
    user_id = message.from_user.id
    print("ошибка после создания user_id")
    if user_id not in user_lang:
        print("ошибка после проверки user_id")
        await message.answer("Please select a language first by typing /start.")
        return
    if user_lang[message.from_user.id] == "RU":
        print("ошибка после проверки языка")
        file_path = "C:\\Users\\marat\\OneDrive\\Рабочий стол\\тгБот\\Motivation-telegram-bot\\RuQuotes.txt"
    elif user_lang[message.from_user.id] == "EN":
        print("ошибка после проверки языка 1")
        file_path = "C:\\Users\\marat\\OneDrive\\Рабочий стол\\тгБот\\Motivation-telegram-bot\\Quotes.txt"
    print("норм после проверки языка")
    
    with open(file_path, "r", encoding="utf-8") as file:
        import random
        quotes = [line.strip() for line in file if line.strip()]
        temp = random.choice(quotes)
        print(type(temp), temp)
        if isinstance(temp, str) and " — " in temp:
            print(type(temp), temp, len(temp))
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