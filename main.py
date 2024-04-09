import asyncio
import logging
from tg_bot.bot import main_bot
from service.service_func import plan_work


# Инициализируем логгер
logger = logging.getLogger(__name__)


async def main():

    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.WARNING,                             # настройка - DEBUG, продакшен - WARNING
        filename="logs.log",                               # добавляем логи в файл
        filemode='a',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting program. Testing: daily - 07:30, 16:30. '
                'Sending and updating the report: monday - 10:00')

    bot_task = asyncio.create_task(main_bot())
    plan_work_task = asyncio.create_task(plan_work())

    print('Программа запущена. Тест в 07:30 и 16:30. '
          'Отправка и обновление отчета в понедельник в 10:00')

    await asyncio.gather(bot_task, plan_work_task)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        logger.exception()
