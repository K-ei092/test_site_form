from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from tg_bot.filters.filters import IsAdmins, IsPrivatChat


router = Router()


# Этот хэндлер будет срабатывать на команду "/admin"
# и отправлять в ответ logs файл
@router.message(Command(commands='admin'), IsAdmins(), IsPrivatChat())
async def process_admin_command(message: Message):
    file = FSInputFile("logs.log")
    await message.answer_document(document=file)
