from random import randint
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import config

bot = Bot(config.TOKEN)
dp = Dispatcher()

attemps = 5
users = {}

# def get_random_number():
#     return randint(1, 100)

@dp.message(CommandStart())
async def start(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {"in game": False,
                                        "secret_number": None,
                                        "attemps": None,
                                        "total_games": 0,
                                        "wins": 0}
        print(users)
    await message.answer(
        f'Привет, давай сыграем, я загадаю число от 1 до 100, а ты его попробуешь угадать за {attemps} попыток'
    )

@dp.message(Command(commands='help'))
async def help(message: Message):
    await message.answer(
        f'''
Правила игры:

Я загадываю число от 1 до 100, а вам нужно его угадать
У вас есть {attemps} попыток

/help - подсказка
/stat - статистика игр
/cancel - выйти из игры'''
    )

@dp.message(Command(commands='stat'))
async def stat(message: Message):
    await message.answer(f'''
Колличество сыгранных игр - {users[message.from_user.id]["total_games"]}
Колличество побед - {users[message.from_user.id]["wins"]}
''')

@dp.message(Command(commands='cancel'))
async def cancel(message: Message):
    if users[message.from_user.id]["wins"]:
        users[message.from_user.id]["wins"] = False
        await message.answer(f'Игра была прервана')
    else:
        await message.answer(f'Мы пока не играем чтобы прервать игру')

@dp.message(F.text.lower().in_(['да','давай','сыграем','игра','хочу играть','давай сыграем']))
async def play_yes(message: Message):
    if not users[message.from_user.id]["in game"]:
        users[message.from_user.id]["in game"] = True
        users[message.from_user.id]["secret_number"] = randint(1, 100)
        users[message.from_user.id]["attemps"] = attemps
        await message.answer(f'Я загадал число от 1 до 100, попробуй отгадать его)')
    else:
        await message.answer(f'Пока мы играем я могу реагировать только на цифры и на комманды')

@dp.message(F.text.lower().in_(['нет','не','не хочу','не надо','потом',]))
async def play_no(message: Message):
    if not users[message.from_user.id]["in game"]:
        await message.answer(f'Жаль, а так хотелось с вами поиграть(')
    else:
        await message.answer(f'Мы сейчас играем, сейчас присылайте мне только числа или комманды')

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def play(message: Message):
    if users[message.from_user.id]["in game"]:
        if int(message.text) == users[message.from_user.id]["secret_number"]:
            users[message.from_user.id]["wins"] += 1
            users[message.from_user.id]["total_games"] += 1
            await message.answer(f"Поздравляю, вы угадали число 🥳")
        elif int(message.text) < users[message.from_user.id]["secret_number"]:
            users[message.from_user.id]["attemps"] -= 1
            await message.answer(f"Не угадали, моё число больше, у вас осталось {users[message.from_user.id]['attemps']} попыток")
        else:
            users[message.from_user.id]["attemps"] -= 1
            await message.answer(f"Не угадали, моё число меньше, у вас осталось {users[message.from_user.id]['attemps']} попыток")

        if users[message.from_user.id]["attemps"] == 0:
            users[message.from_user.id]["in game"] = False
            users[message.from_user.id]["total_games"] += 1
            await message.answer(f"Увы, но вы проиграли")
    else:
        await message.answer(f"Мы ещё не начали играть")

@dp.message()
async def process_other_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('''
Мы же сейчас с вами играем.
Присылайте, пожалуйста, числа от 1 до 100''')
    else:
        await message.answer('''
Я довольно ограниченный бот, давайте
просто сыграем в игру?''')

if __name__ == '__main__':
    dp.run_polling(bot)
