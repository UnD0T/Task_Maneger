import asyncio
import json

import aiofiles
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import as_marked_section, Underline, Bold, as_key_value
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboard.for_navigate import task_keyboard
from filters.Filters import ChatTypeFilter

task_router = Router()
task_router.message.filter(ChatTypeFilter(['private']))


async def read_file():
    async with aiofiles.open('./tasks.json', encoding='utf-8') as file:
        data = await file.read()
        json_data = json.loads(data)
    return json_data


async def write_file(data):
    async with aiofiles.open('./tasks.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data, indent=4))


@task_router.message(Command('tasks'))
async def homeworks_cmd(message: types.Message):
    await message.answer('Яку дію виконати з завданнями?', reply_markup=task_keyboard)


@task_router.message(F.text == 'view all tasks')
async def all_homeworks_cmd(message: types.Message):
    task_list = await read_file()
    for i in await read_file():
        text = as_marked_section(
            Underline(Bold('Task')),
            as_key_value('Тема ', i['topic']),
            as_key_value('Дедлайн ', i['deadline']),
            as_key_value('Завдання ', i['task']),
            as_key_value('Додатковий матеріал ', i['aditional']),
            marker='📌 '
        )
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(text='видалити завдання', callback_data=f'delete_{task_list.index(i)}')
        )

        await message.answer(text.as_html(), reply_markup=builder.as_markup())
        await asyncio.sleep(0.3)


@task_router.callback_query(F.data.split('_')[0] == 'delete')
async def del_homework(callback: types.CallbackQuery):  # 'delete_1'
    homework_id = callback.data.split('_')[-1]
    homeworks_list = await read_file()  # []
    homeworks_list.pop(int(homework_id))
    await write_file(homeworks_list)
    await callback.message.answer('Завдання видалено!')
    await callback.answer('Its ok, task has been deleted', show_alert=True)


class AddTask(StatesGroup):
    topic = State()
    deadline = State()
    task = State()
    aditional_material = State()


@task_router.message(StateFilter(None), F.text == 'add new task')
async def add_homeworks_cmd(message: types.Message, state: FSMContext):
    await message.answer('Введіть тему завдання: ', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddTask.topic)


@task_router.message(Command("cancel"))
@task_router.message(F.text.casefold() == "cancel")
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


@task_router.message(AddTask.topic, F.text)
async def add_number_cmd(message: types.Message, state: FSMContext):
    await state.update_data(topic=message.text)
    await message.answer('Введіть дедлайн завдання: ')
    await state.set_state(AddTask.deadline)


@task_router.message(AddTask.deadline, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    await message.answer('Введіть завдання: ')
    await state.set_state(AddTask.task)


@task_router.message(AddTask.task, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(task=message.text)
    await message.answer('Введіть важливі деталі по завданю: ')
    await state.set_state(AddTask.aditional_material)


@task_router.message(AddTask.aditional_material, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(aditional=message.text)
    await message.answer('Завдання додано!', reply_markup=task_keyboard)
    data = await state.get_data()
    data_to_update = await read_file()
    data_to_update.append(data)
    await write_file(data_to_update)
    await message.answer(str(data))
    await state.clear()
