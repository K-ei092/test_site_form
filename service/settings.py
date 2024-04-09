from service.proxy_for_chrom import create_plugin
import service


def set_settings():

    hl = input('Включить фоновый режим работы браузера? Введите Y/n  >>>>>')
    px = input('Включить прокси? (для включения функции вам понадобятся логин, пароль, '
               'хост и порт прокси (с аутентификацией))/ Включить? Введите: Y/n  >>>>>>')
    if hl == 'Y':
        service.flags.headless = True

    if px == 'Y':
        old_proxy = input(
            'Если вы ранее настраивали порт proxy, и хотите оставить прежние '
            'настройки, то наберите "Y", в обратном случае - "n"  >>>>>'
        )
        if old_proxy == 'Y':
            service.flags.proxies = True
        else:
            create_plugin()
            service.flags.proxies = True