# путем запуска в Python код создает (обновляет) новый плагин 'proxy_auth_plugin.zip'
# для Chrom, который используется для прокси с аутентификацией
import zipfile

def create_plugin():
    PROXY_HOST = input('введите PROXY HOST (диапазон от 0 до 255) в формате: 0.0.0.0     >')
    PROXY_PORT = int(input('введите PROXY PORT (диапазон от 0 до 65535) в формате: 00000     >'))
    PROXY_USER = input('введите PROXY USER     >')
    PROXY_PASS = input('введите PROXY PASS     >')

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    print('плагин "proxy_auth_plugin.zip" с настройками прокси сохранен в основной директории')

if __name__ == '__main__':
    create_plugin()