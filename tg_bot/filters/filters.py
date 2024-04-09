from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message

from config_data.config import ConfigTgBot, load_config_tg_bot

config: ConfigTgBot = load_config_tg_bot()
chat_ids: list[int] = config.config_tg_bot.chat_ids
admin_ids: list[int] = config.config_tg_bot.admin_ids


# фильтр проверяет подписку на чат/канал
class IsSubscriber(BaseFilter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        for chat_id in chat_ids:
            sub = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
            if sub.status != 'left':
                return True
        return False


# фильтр проверят на админа
class IsAdmins(BaseFilter):
    def __init__(self) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


# фильтр проверяет приватный ли чат
class IsPrivatChat(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.type == 'private':
            return True
        else:
            return False
