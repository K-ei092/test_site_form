from config_data.config import ConfigTgBot, load_config_tg_bot
from memory_profiler import memory_usage
import requests


config: ConfigTgBot = load_config_tg_bot()
chat_id: int = config.config_tg_bot.chat_ids[0]
bot_token = config.config_tg_bot.token_tg_bot

def api_send_message(text):
    requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates?offset=-1')
    message = text
    url = f'https://api.telegram.org/bot{bot_token}/'
    api_url_send_message = url + f'sendMessage?chat_id={str(chat_id)}&text={message}'
    response = requests.get(api_url_send_message)
    if 200 <= response.status_code <= 205:
        pass
    else:
        api_send_message(message)


def api_send_memory():
    requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates?offset=-1')
    memory = memory_usage()
    url = f'https://api.telegram.org/bot{bot_token}/'
    api_url_send_memory = url + f'sendMessage?chat_id={str(chat_id)}&text=потребление памяти - {memory} МБ'
    response = requests.get(api_url_send_memory)
    if 200 <= response.status_code <= 205:
        pass
    else:
        api_send_memory()


def api_send_result():
    requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates?offset=-1')
    file_path = 'result_work.xlsx'
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument?chat_id={str(chat_id)}'

    with open(file_path, 'rb') as file:
        files = {'document': file}
        response = requests.get(url, files=files)

    if 200 <= response.status_code <= 205:
        pass
    else:
        api_send_result()
