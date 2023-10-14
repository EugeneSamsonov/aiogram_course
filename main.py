from random import randint
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import config

bot = Bot(config.TOKEN)
dp = Dispatcher()

attemps = 5
user = {'in game': False,
        'secret_number': None,
        'attemps': None,
        'total_games': 0,
        'wins': 0}

def get_random_number():
    return randint(1, 100)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f'Привет, давай сыграем, я загадаю число от 1 до 100, а ты его попробуешь угадать за {attemps} попыток'
    )

@dp.message(Command(commands='help'))
async def help(message: Message):
    await message.answer(
        f'''Я загадываю число, а ты пытаешься его угадать, чтобы начать просто напиши "Да", "Давай", "Сыграем"
        /start - старт бота
        /help - подсказка
        /stat - статистика игр
        /cancel - выйти из игры'''
    )

if __name__ == '__main__':
    dp.run_polling(bot)
