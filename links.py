import asyncio
import json

import aiofiles
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import as_marked_section, Underline, Bold, as_key_value
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboard.for_navigate import link_keyboard
from filters.Filters import ChatTypeFilter

link_router = Router()
link_router.message.filter(ChatTypeFilter(['private']))


async def read_file():
    async with aiofiles.open('./links.json', encoding='utf-8') as file:
        data = await file.read()
        json_data = json.loads(data)
    return json_data


async def write_file(data):
    async with aiofiles.open('./links.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data, indent=4))


@link_router.message(Command('links'))
async def homeworks_cmd(message: types.Message):
    await message.answer('Яку дію виконати з ссилками?', reply_markup=link_keyboard)


@link_router.message(F.text == 'view all links')
async def all_homeworks_cmd(message: types.Message):
    task_list = await read_file()
    for i in await read_file():
        text = as_marked_section(
            Underline(Bold('Link')),
            as_key_value('Ссилка ', i['link']),
            as_key_value('Інформація ', i['info']),
            marker='📌 '
        )
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(text='видалити ссилку', callback_data=f'delete_{task_list.index(i)}')
        )

        await message.answer(text.as_html(), reply_markup=builder.as_markup())
        await asyncio.sleep(0.3)


@link_router.callback_query(F.data.split('_')[0] == 'delete')
async def del_homework(callback: types.CallbackQuery):  # 'delete_1'
    homework_id = callback.data.split('_')[-1]
    homeworks_list = await read_file()  # []
    homeworks_list.pop(int(homework_id))
    await write_file(homeworks_list)
    await callback.message.answer('Ссилку видалено!')
    await callback.answer('Its ok, task has been deleted', show_alert=True)


class AddLink(StatesGroup):
    link = State()
    info = State()


@link_router.message(StateFilter(None), F.text == 'add new link')
async def add_homeworks_cmd(message: types.Message, state: FSMContext):
    await message.answer('Введіть ссилку: ', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddLink.link)


@link_router.message(Command("cancel"))
@link_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@link_router.message(AddLink.link, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(task=message.text)
    await message.answer('Введіть інформацію по ссилці: ')
    await state.set_state(AddLink.info)


@link_router.message(AddLink.info, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(aditional=message.text)
    await message.answer('Ссилку додано!', reply_markup=link_keyboard)
    data = await state.get_data()
    data_to_update = await read_file()
    data_to_update.append(data)
    await write_file(data_to_update)
    await message.answer(str(data))
    await state.clear()
