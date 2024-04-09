from dataclasses import dataclass
from environs import Env


@dataclass(slots=True, frozen=True)
class Mail:
    email: str
    password: str
    imap: str


@dataclass(slots=True, frozen=True)
class ConfigMail:
    config_mail: Mail


@dataclass(slots=True, frozen=True)
class TgBot:
    token_tg_bot: str
    chat_ids: list[int]
    admin_ids: list[int]


@dataclass(slots=True, frozen=True)
class ConfigTgBot:
    config_tg_bot: TgBot


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями email, password и imap
def load_config_mail(path: str = './.env') -> ConfigMail:
    env = Env()
    env.read_env(path)
    return ConfigMail(
        config_mail=Mail(
            email=env('EMAIL'),
            password=env('EMAIL_PASSWORD'),
            imap=env('IMAP')
        )
    )


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token_tg_bot, admin_ids и chat_ids
def load_config_tg_bot(path: str = './.env') -> ConfigTgBot:
    env = Env()
    env.read_env(path)
    return ConfigTgBot(
        config_tg_bot=TgBot(
            token_tg_bot=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            chat_ids=list(map(int, env.list('CHAT_IDS')))
        )
    )
