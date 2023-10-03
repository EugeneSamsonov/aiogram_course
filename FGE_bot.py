from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import config

bot = Bot(config.TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def start_command(message: Message):
    await message.answer('Привет я эхо-бот')

@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer('Напиши мне что-нибудь')

@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy'
        )




if __name__ == '__main__':
    dp.run_polling(bot)
