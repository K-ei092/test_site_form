import random
import time
import sys
import os
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromiumService
from service.settings import set_settings
from webdriver_manager.chrome import ChromeDriverManager
import service


set_settings()


tuple_user_agent_mob = ("Samsung Galaxy S8+", "Galaxy S8", "iPhone SE", "iPhone 12 Pro",
                        "Samsung Galaxy S20 Ultra", "Galaxy Note 3", "Galaxy S9+",
                        "Galaxy S5", "Nexus 6")

tuple_user_agent_pc = (
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.66 (Edition Yx)",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Brave/1.18.77 Chrome/87.0.4280.141",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edge/88.0.705.50",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 YaBrowser/20.12.2.107 Yowser/2.5 Safari/537.36")


class SiteTest:
    current_dir = os.getcwd()
    folder_name = 'seleniumwire_storage'
    storage_dir = os.path.join(current_dir, folder_name)
    optionsSW = {
        'request_storage_base_dir': storage_dir,
        'request_storage': 'memory',
        'request_storage_max_size': 200  # 'log_level': None
    }
    ET_path = ChromiumService(ChromeDriverManager().install())

    # конструктор вебдрайвера
    def __init__(self,
                 n: int = random.randint(0, 1),
                 headless: bool = service.flags.headless,
                 proxy: bool = service.flags.proxies):

        user_agent_rand = (random.choice(tuple_user_agent_mob), random.choice(tuple_user_agent_pc))
        self.ua = user_agent_rand[n]
        self.n = n

        option = webdriver.ChromeOptions()
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument('log-level=3')
        option.add_argument('--window-size=1300,750')
        option.set_capability("pageLoadStrategy", "eager")  # не ждать полной загрузки страницы
        if headless:
            option.add_argument('--headless=new')  # включение фонового режима
        if proxy:
            option.add_extension('proxy_auth_plugin.zip')  # добавляем плагин с настройками прокси с аутификацией
        if self.n == 0:
            mobile_emulation = {"deviceName": self.ua}
            option.add_experimental_option("mobileEmulation", mobile_emulation)

        else:
            option.add_argument(f'user-agent={self.ua}')

        self.driver = webdriver.Chrome(
            service=self.ET_path,
            options=option,
            seleniumwire_options=self.optionsSW
        )
        self.driver.implicitly_wait(10)

    @staticmethod
    def _shape_result(name_form, status_code, response_date, user_agent):

        if 200 <= int(status_code) <= 399:
            return (
                str(status_code),
                f'{name_form}',
                response_date,
                user_agent
            )
        else:
            return (
                '0',
                f'{name_form} (ошибка сайта)',
                f'Форма не отправлена. Ответ сайта - {str(status_code)}',
                user_agent
            )

    @staticmethod
    def _report_bug(name_form, sys_exp_info, user_agent):

        if 'Message: no such element: Unable to locate element:' in str(sys_exp_info) \
                or 'Message: element not interactable' in str(sys_exp_info) \
                or 'Message: element click intercepted' in str(sys_exp_info) \
                or 'Message: no such element' in str(sys_exp_info):
            return (
                '0',
                f'{name_form} (ошибка программы)',
                f'Не обнаружен или не заполнен элемент на странице: {str(sys_exp_info)}',
                user_agent
            )

        elif "object has no attribute 'status_code'" in str(sys_exp_info):
            return (
                'Сайт не дал ответа',
                f'{name_form}',
                time.strftime('%m/%d/%y %H:%M:%S', time.localtime(time.time())),
                user_agent
            )
        else:
            return (
                '0',
                f'{name_form} (неизвестная ошибка)',
                f'неизвестная ошибка при работе с сайтом - {str(sys_exp_info)}',
                user_agent
            )

    def check_mm_novuy_2(self, namber_test: str) -> tuple:

        try:

            with self.driver as WD:

                WD.get("https://www.example.ru/1")
                time.sleep(1)
                WD.execute_script("document.body.style.zoom='60%'")
                html = WD.find_element(By.TAG_NAME, 'html')
                for _ in range(2):
                    html.send_keys(Keys.DOWN)
                time.sleep(2)
                button_field_manager = WD.find_element(By.CSS_SELECTOR, 'a.open_popup')
                if button_field_manager:
                    time.sleep(15)
                    WD.execute_script("window.stop();")
                WD.execute_script("arguments[0].click();", button_field_manager)
                time.sleep(1)
                form = WD.find_element(By.CSS_SELECTOR, '#lightbox-wrap')
                form_your_name = form.find_element(By.CSS_SELECTOR, 'input#userName')
                for k in namber_test:
                    form_your_name.send_keys(k)
                    time.sleep(0.06)
                form_contact_namber = form.find_element(By.CSS_SELECTOR, 'input#userTelephone')
                time.sleep((random.randint(1, 4)))
                WD.execute_script("arguments[0].value = arguments[1];", form_contact_namber, '+1 (111) 111-11-11')
                button_order = form.find_element(By.CSS_SELECTOR, '#submitButton')
                time.sleep(2)
                WD.execute_script("arguments[0].click();", button_order)
                time.sleep(6)
                response_page = WD.requests[-1]
                time.sleep(3)
                status_code, response_date = response_page.response.status_code, response_page.date.strftime('%x %X')
                time.sleep(5)

                return self._shape_result('form_mm_novuy_2', status_code, response_date, self.ua)

        except Exception:

            return self._report_bug('form_mm_novuy_2', sys.exc_info()[1], self.ua)

    def check_zakazat_zvonok_3(self, namber_test: str) -> tuple:

        try:

            with self.driver as WD:

                WD.get("https://www.example.ru/2")
                time.sleep(1)
                WD.execute_script("document.body.style.zoom='60%'")
                html = WD.find_element(By.TAG_NAME, 'html')
                if self.n == 0:
                    for _ in range(70):
                        html.send_keys(Keys.DOWN)
                else:
                    for _ in range(45):
                        html.send_keys(Keys.DOWN)
                time.sleep(1)
                sector = WD.find_element(By.CSS_SELECTOR, '#call-button-box')
                button_order_call = sector.find_element(By.CSS_SELECTOR, '#tcall-button-box > a')
                if button_order_call:
                    time.sleep(10)
                    WD.execute_script("window.stop();")
                WD.execute_script("arguments[0].click();", button_order_call)
                time.sleep(3)
                form = WD.find_element(By.CSS_SELECTOR, '#lightbox-wrap')
                form_your_name = form.find_element(By.CSS_SELECTOR, '#userName')
                for k in namber_test:
                    form_your_name.send_keys(k)
                    time.sleep(0.07)
                form_contact_namber = form.find_element(By.CSS_SELECTOR, '#userTelephone')
                time.sleep((random.randint(3, 6)))
                WD.execute_script("arguments[0].value = arguments[1];", form_contact_namber, '+1 (111) 111-11-11')
                button_order_call_finish = form.find_element(By.CSS_SELECTOR, '#submitButton')
                time.sleep(3)
                WD.execute_script("arguments[0].click();", button_order_call_finish)
                time.sleep(7)
                response_page = WD.requests[-1]
                time.sleep(3)
                status_code, response_date = response_page.response.status_code, response_page.date.strftime('%x %X')
                time.sleep(5)

                return self._shape_result('form_zakazat_zvonok_3', status_code, response_date, self.ua)

        except Exception:

            return self._report_bug('form_zakazat_zvonok_3', sys.exc_info()[1], self.ua)

    def check_consultation_4(self, namber_test: str) -> tuple:

        try:

            with self.driver as WD:

                WD.get("https://www.example.ru/3")
                time.sleep(1)
                WD.execute_script("document.body.style.zoom='60%'")
                html = WD.find_element(By.TAG_NAME, 'html')
                if self.n == 0:
                    for _ in range(4):
                        html.send_keys(Keys.DOWN)
                else:
                    for _ in range(7):
                        html.send_keys(Keys.DOWN)
                time.sleep(1)
                string_fence_length = html.find_element(By.CSS_SELECTOR, 'input.input')
                string_fence_length.send_keys(str(random.randint(30, 50)))
                time.sleep(2)
                for _ in range(6):
                    html.send_keys(Keys.DOWN)
                time.sleep(2)
                button_calculate = WD.find_element(By.CSS_SELECTOR, 'input.trigga')
                WD.execute_script("arguments[0].click();", button_calculate)
                time.sleep(2)
                for _ in range(4):
                    html.send_keys(Keys.DOWN)

                if self.n == 0:
                    time.sleep(1)
                    page = WD.find_element(By.CSS_SELECTOR, '#mobileCalcResult__buttons')
                    button_get_consultation = page.find_element(By.CSS_SELECTOR, '#proflist.button_call')
                    WD.execute_script("arguments[0].click();", button_get_consultation)

                else:
                    time.sleep(2)
                    button_get_consultation = WD.find_element(By.CSS_SELECTOR, 'div.custom_width')
                    WD.execute_script("arguments[0].click();", button_get_consultation)
                time.sleep(3)
                form = WD.find_element(By.CSS_SELECTOR, '#lightbox-outer')
                form_your_name = form.find_element(By.CSS_SELECTOR, '#userName')
                for k in namber_test:
                    form_your_name.send_keys(k)
                    time.sleep(0.04)
                for _ in range(4):
                    html.send_keys(Keys.DOWN)
                form_contact_namber = form.find_element(By.CSS_SELECTOR, 'input#userTelephone')
                time.sleep((random.randint(1, 4)))
                WD.execute_script("arguments[0].value = arguments[1];", form_contact_namber, '+1 (111) 111-11-11')
                time.sleep(1)
                button_send = form.find_element(By.CSS_SELECTOR, '#submitButton')
                time.sleep(3)
                WD.execute_script("arguments[0].click();", button_send)
                time.sleep(5)
                response_page = WD.requests[-1]
                time.sleep(5)
                status_code, response_date = response_page.response.status_code, response_page.date.strftime('%x %X')
                time.sleep(5)

                return self._shape_result('form_consultation_4', status_code, response_date, self.ua)

        except Exception:

            return self._report_bug('form_consultation_4', sys.exc_info()[1], self.ua)


    def get_methods(self):
        return (self.check_mm_novuy_2, self.check_zakazat_zvonok_3, self.check_consultation_4)

    # закрытие драйвера
    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def __del__(self):
        pass
