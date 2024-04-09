import asyncio

from aiogram import Bot, Dispatcher
from tg_bot.handlers import other_handlers, user_handlers, admin_handlers
from tg_bot.keyboards.main_menu import set_main_menu

from config_data.config import ConfigTgBot, load_config_tg_bot


# Функция конфигурирования и запуска бота
async def main_bot():

    # Загружаем конфиг в переменную config
    config: ConfigTgBot = load_config_tg_bot()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.config_tg_bot.token_tg_bot,
                   parse_mode='HTML')      # 'MarkdownV2'
    dp = Dispatcher()

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main_bot())
