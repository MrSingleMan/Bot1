from aiogram import types

buttons1 = types.KeyboardButton(text='/start')
buttons2 = types.KeyboardButton(text='/stop')
buttons3 = types.KeyboardButton(text='/info')
buttons4 = types.KeyboardButton(text='Покажи лису')
buttons5 = types.KeyboardButton(text='/игра')

keyboard1 = [
    [buttons1, buttons2, buttons3,],
    [buttons4, buttons5]
]

keyboard = types.ReplyKeyboardMarkup(keyboard=keyboard1, resize_keyboard=True)