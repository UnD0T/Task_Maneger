from aiogram import types, Router, F
# from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import ReplyKeyboardRemove
from filters.Filters import ChatTypeFilter
from keyboard.for_navigate import keyboard
# from aiogram.utils.formatting import as_marked_section, Bold, TextLink
private_router = Router()
private_router.message.filter(ChatTypeFilter(['private']))


@private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('this answer for start command', reply_markup=keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Choose your command'
    ))


@private_router.message(or_f(Command('keyboard_remove'), F.text.lower() == 'keyboard_remove'))
async def options_cmd(message: types.Message):
    await message.answer('Your keyboard has been removed', reply_markup=ReplyKeyboardRemove())


@private_router.message(Command('about'))
async def options_cmd(message: types.Message):
    await message.answer('info about <b><u>bot</u></b>')


@private_router.message((F.text.lower() == 'розклад') | (F.text.contains('schedule')))
@private_router.message(Command('schedule'))
async def schedule_cmd(message: types.Message):
    await message.answer('our current schedule:'
                         ' Monday: 18:00-19:30 IT / 19:30-20:30 SOFT'
                         ' Wednesday: 18:00-19:30 IT ')
