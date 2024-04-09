from aiogram import Router
from aiogram.types import Message
from tg_bot.filters.filters import IsPrivatChat
from config_data.config import ConfigTgBot, load_config_tg_bot

config: ConfigTgBot = load_config_tg_bot()
chat_id: int = config.config_tg_bot.chat_ids[0]

router = Router()

# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message(IsPrivatChat())
async def send_echo(message: Message):
    await message.bot.send_message(
        chat_id=chat_id,
        text=f'Мне неизвестна команда "{message.text}"\n'
        )