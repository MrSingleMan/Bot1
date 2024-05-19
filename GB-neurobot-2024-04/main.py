import asyncio
import config
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import logging
import random
from keyboards import keyboard
from random_fox import fox


#Логирование
logging.basicConfig(level=logging.INFO)

# Объект бота и диспетчера
bot = Bot(token=config.token)
dp = Dispatcher()

# Словарь для хранения данных об игре
user_games ={}

# Хэндлер на команду /start
@dp.message(Command(commands=['start']))
async def start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=keyboard)

@dp.message(Command(commands=['стоп']))
@dp.message(Command(commands=['stop']))
async def stop(message: types.Message):
    print(message.from_user.full_name)
    await message.answer(f'Пока, {message.chat.first_name}!')

# Хэндлер на команду /info
@dp.message(Command(commands=['info', 'инфо']))
@dp.message(F.text.lower() == 'инфо')
async def info(message: types.Message):
    info_text = (
        "🤖 *Информация о боте*\n\n"
        "Этот бот может выполнять следующие команды:\n"
        "/start - Начать взаимодействие с ботом\n"
        "/stop - Остановить взаимодействие с ботом\n"
        "/info - Получить информацию о боте\n\n"
        "/игра - Запустить игру 'Угадай число'\n\n"
        "покажи лису - Получить случайное изображение лисы\n\n"
    )
    await message.answer(info_text, parse_mode='Markdown')

# Хэндлер на команду /game
@dp.message(Command(commands=['игра']))
async def start_game(message: types.Message):
    user_id = message.from_user.id
    user_games[user_id] = {
        'number': random.randint(1, 10),
        'attempts': 3
    }
    await message.answer('Я загадал число от 1 до 10. Попробуй угадать его! У тебя 3 попытки.')

@dp.message(F.text.lower() == 'покажи лису')
async def info(message: types.Message):
    img_fox = fox()
    await message.answer('Привет, лови лису')
    await message.answer_photo(img_fox)

# Хэндлер для обработки попыток угадать число
@dp.message()
async def guess_number(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_games:
        return

    try:
        guess = int(message.text)
    except ValueError:
        await message.reply('Пожалуйста, введи число от 1 до 10.')
        return

    game = user_games[user_id]
    if guess < 1 or guess > 10:
        await message.reply('Пожалуйста, введи число от 1 до 10.')
        return

    if guess == game['number']:
        await message.answer('Поздравляю! Ты угадал число!')
        del user_games[user_id]
    else:
        game['attempts'] -= 1
        if game['attempts'] > 0:
            hint = 'меньше' if guess > game['number'] else 'больше'
            await message.answer(f'Неправильно! Загаданное число {hint} {guess}. У тебя осталось {game["attempts"]} попыток.')
        else:
            await message.answer(f'Ты проиграл! Я загадал число {game["number"]}.')
            del user_games[user_id]




async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())