from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# keyboard = types.ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             types.KeyboardButton(text='options'),
#             types.KeyboardButton(text='schedule'),
#         ],
#         [
#             types.KeyboardButton(text='links'),
#             types.KeyboardButton(text='homeworks'),
#         ],
#         [
#             types.KeyboardButton(text='about'),
#         ]
#     ],
#     resize_keyboard=True,
#     input_field_placeholder='Choose your command'
# )

keyboard = ReplyKeyboardBuilder()
keyboard.add(
    types.KeyboardButton(text='options'),
    types.KeyboardButton(text='schedule'),
    types.KeyboardButton(text='links'),
    types.KeyboardButton(text='homeworks'),
    types.KeyboardButton(text='about'),
)
keyboard.adjust(3, 2)

task_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text='view all tasks'),
        ],
        [
            types.KeyboardButton(text='add new task'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose your option'
)

link_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text='view all links'),
        ],
        [
            types.KeyboardButton(text='add new link'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose your option'
)
