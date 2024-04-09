from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from tg_bot.filters.filters import IsSubscriber
from tg_bot.lexicon.lexicon import LEXICON

from config_data.config import ConfigTgBot, load_config_tg_bot
from service import flags
from service.main_test import main_test
from memory_profiler import memory_usage


config: ConfigTgBot = load_config_tg_bot()
chat_id: int = config.config_tg_bot.chat_ids[0]

router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart(), IsSubscriber())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON[message.text]
    )


# Этот хэндлер будет срабатывать на команду "/help"
@router.message(F.text.startswith('/help'), IsSubscriber())
async def process_help_command(message: Message):
    await message.bot.send_message(
        chat_id=chat_id,
        text=LEXICON[message.text]
    )


# Этот хэндлер будет срабатывать на команду "/formshelp"
@router.message(F.text.startswith('/formshelp'), IsSubscriber())
async def process_helpforms_command(message: Message):
    await message.bot.send_message(
        chat_id=chat_id,
        text=LEXICON[message.text]
    )


# Этот хэндлер будет срабатывать на команду "/offschedule"
@router.message(F.text.startswith('/offschedule'), IsSubscriber())
async def process_offschedule_command(message: Message):
    flags.flag_scheduled_check = False
    await message.bot.send_message(
        chat_id=chat_id,
        text=LEXICON[message.text]
    )


# Этот хэндлер будет срабатывать на команду "/onschedule"
@router.message(F.text.startswith('/onschedule'), IsSubscriber())
async def process_onschedule_command(message: Message):
    flags.flag_scheduled_check = True
    await message.bot.send_message(
        chat_id=chat_id,
        text=LEXICON[message.text]
    )


# Этот хэндлер будет срабатывать на команду "/stop"
@router.message(F.text.startswith('/stop'), IsSubscriber())
async def process_stop_command(message: Message):
    await message.bot.send_message(
        chat_id=chat_id,
        text=LEXICON[message.text]
    )
    flags.flag_work_script = False


# Этот хэндлер будет срабатывать на команду "/memory"
@router.message(F.text.startswith('/memory'), IsSubscriber())
async def process_memory_command(message: Message):
    memory = memory_usage()
    await message.bot.send_message(
        chat_id=chat_id,
        text=f'потребление памяти - {memory} МБ'
    )


# Этот хэндлер будет срабатывать на команду "/testmob"
@router.message(F.text.startswith('/testmob'), IsSubscriber())
async def process_testmob_command(message: Message):
    if not flags.flag_process_started:
        await message.bot.send_message(
            chat_id=chat_id,
            text=LEXICON[message.text]
        )
        await main_test(0)
    else:
        await message.bot.send_message(
            chat_id=chat_id,
            text='В настоящее время осуществляется проверка мобильной версии сайта. Пожалуйста, дождитесь завершения'
        )


# Этот хэндлер будет срабатывать на команду "/testpc"
@router.message(F.text.startswith('/testpc'), IsSubscriber())
async def process_testpc_command(message: Message):
    if not flags.flag_process_started:
        await message.bot.send_message(
            chat_id=chat_id,
            text=LEXICON[message.text]
        )
        await main_test(1)
    else:
        await message.bot.send_message(
            chat_id=chat_id,
            text='В настоящее время осуществляется проверка ПК версии сайта. Пожалуйста, дождитесь завершения'
        )


# Этот хэндлер будет срабатывать на команду "/result"
@router.message(F.text.startswith('/result'), IsSubscriber())
async def process_result_command(message: Message):
    file = FSInputFile("result_work.xlsx")
    await message.bot.send_document(
        chat_id=chat_id, document=file
    )


# Этот хэндлер будет срабатывать на команду "/instruction"
@router.message(F.text.startswith('/instruction'), IsSubscriber())
async def process_instruction_command(message: Message):
    file = FSInputFile("README.txt")
    await message.bot.send_document(
        chat_id=chat_id, document=file
    )
