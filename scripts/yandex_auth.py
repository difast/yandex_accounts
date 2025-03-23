import time
import logging


class YandexAuth:
    def __init__(self, adb_manager):
        self.adb = adb_manager
        self.current_password = None  # Текущий пароль (можно установить при авторизации)

    def find_element_and_click(self, resource_id):
        """Находит элемент по resource-id и выполняет клик."""
        # Получаем информацию о элементе
        ui_dump = self.adb.run_adb_command("shell uiautomator dump /sdcard/ui.xml")
        if "UI hierchary dumped to" not in ui_dump:
            logging.error("Не удалось получить UI-иерархию")
            return False
        
        # Читаем файл с UI-иерархией
        ui_xml = self.adb.run_adb_command("shell cat /sdcard/ui.xml")
        
        # Ищем элемент по resource-id
        if f'resource-id="{resource_id}"' not in ui_xml:
            logging.error(f"Элемент с resource-id={resource_id} не найден")
            return False
        
        # Парсим координаты элемента
        bounds_start = ui_xml.find(f'bounds="', ui_xml.find(f'resource-id="{resource_id}"'))
        bounds_end = ui_xml.find('"', bounds_start + len('bounds="') + 1)
        bounds = ui_xml[bounds_start + len('bounds="'):bounds_end]
        
        # Извлекаем координаты
        x1, y1, x2, y2 = map(int, bounds.replace("][", ",").split(","))
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        
        # Выполняем клик по центру элемента
        self.adb.run_adb_command(f"shell input tap {center_x} {center_y}")
        logging.info(f"Клик по элементу {resource_id} на координатах ({center_x}, {center_y})")
        return True



    def login_to_browser(self, login, password, twofa_code=None):
        """Авторизация в Яндекс.Браузере с поддержкой 2FA."""
        # Запуск браузера
        self.adb.run_adb_command("shell am start -n com.yandex.browser/.YandexBrowserActivity")
        time.sleep(2)  # Ждем загрузки браузера
        
        # Ввод логина
        self.adb.run_adb_command("shell input tap 300 500")  # Клик в поле логина
        self.adb.run_adb_command(f"shell input text {login}")
        self.adb.run_adb_command("shell input keyevent 66")  # Enter
        
        # Ввод пароля
        self.adb.run_adb_command("shell input tap 300 600")  # Клик в поле пароля
        self.adb.run_adb_command(f"shell input text {password}")
        self.adb.run_adb_command("shell input keyevent 66")  # Enter
        
        # Ввод 2FA (если код передан)
        if twofa_code:
            self.adb.run_adb_command("shell input tap 300 700")  # Клик в поле 2FA
            self.adb.run_adb_command(f"shell input text {twofa_code}")
            self.adb.run_adb_command("shell input keyevent 66")  # Enter
        
        logging.info(f"Успешная авторизация для аккаунта {login}")

    def change_password_via_app(self, new_password):
        """Меняет пароль через приложение Яндекс."""
        # Открываем приложение Яндекс
        self.adb.run_adb_command("shell am start -n ru.yandex.searchplugin/.MainActivity")
        time.sleep(2)  # Ждем загрузки приложения
        
        # Переход в настройки аккаунта
        self.adb.run_adb_command("shell input tap 1000 100")  # Клик на аватар
        time.sleep(1)
        self.adb.run_adb_command("shell input tap 500 800")  # Клик на "Настройки"
        time.sleep(1)
        self.adb.run_adb_command("shell input tap 500 600")  # Клик на "Безопасность"
        time.sleep(1)
        self.adb.run_adb_command("shell input tap 500 700")  # Клик на "Смена пароля"
        time.sleep(1)
        
        # Ввод старого пароля
        self.adb.run_adb_command("shell input tap 300 500")  # Клик в поле старого пароля
        self.adb.run_adb_command(f"shell input text {self.current_password}")  # Ввод старого пароля
        self.adb.run_adb_command("shell input keyevent 66")  # Enter
        
        # Ввод нового пароля
        self.adb.run_adb_command("shell input tap 300 600")  # Клик в поле нового пароля
        self.adb.run_adb_command(f"shell input text {new_password}")  # Ввод нового пароля
        self.adb.run_adb_command("shell input keyevent 66")  # Enter
        
        # Подтверждение смены пароля
        self.adb.run_adb_command("shell input tap 300 700")  # Клик на кнопку "Сохранить"
        logging.info("Пароль успешно изменен через приложение")

    def generate_backup_codes_via_app(self):
        """Генерирует резервные коды через приложение Яндекс."""
        # Открываем приложение Яндекс
        self.adb.run_adb_command("shell am start -n ru.yandex.searchplugin/.MainActivity")
        time.sleep(2)  # Ждем загрузки приложения
        
        # Переход в настройки аккаунта
        self.adb.run_adb_command("shell input tap 1000 100")  # Клик на аватар
        time.sleep(1)
        self.adb.run_adb_command("shell input tap 500 800")  # Клик на "Настройки"
        time.sleep(1)
        self.adb.run_adb_command("shell input tap 500 600")  # Клик на "Безопасность"
        time.sleep(1)
        self.adb.run_adb_command("shell input tap 500 700")  # Клик на "Резервные коды"
        time.sleep(1)
        
        # Генерация резервных кодов
        self.adb.run_adb_command("shell input tap 300 500")  # Клик на "Создать резервные коды"
        logging.info("Резервные коды созданы через приложение")

    def login_to_taxi(self, login, password):
        """Авторизация в Яндекс.Такси."""
        # Запуск приложения Яндекс.Такси
        self.adb.run_adb_command("shell am start -n ru.yandex.taxi/.MainActivity")
        time.sleep(2)  # Ждем загрузки приложения
        
        # Клик на кнопку "Войти"
        self.adb.run_adb_command("shell input tap 300 500")
        
        # Ввод логина и пароля
        self.adb.run_adb_command("shell input tap 300 600")  # Клик в поле логина
        self.adb.run_adb_command(f"shell input text {login}")
        self.adb.run_adb_command("shell input keyevent 66")  # Enter
        
        self.adb.run_adb_command("shell input tap 300 700")  # Клик в поле пароля
        self.adb.run_adb_command(f"shell input text {password}")
        self.adb.run_adb_command("shell input keyevent 66")  # Enter
        
        logging.info("Успешная авторизация в Яндекс.Такси")

    def simulate_activity(self):
        """Имитирует активность пользователя."""
        # Открытие случайной страницы
        self.adb.run_adb_command("shell input keyevent 64")  # Открыть браузер
        self.adb.run_adb_command("shell input text 'https://yandex.ru/news'")
        self.adb.run_adb_command("shell input keyevent 66")  # Enter
        
        # Случайные клики
        import random
        for _ in range(5):
            x = random.randint(100, 500)
            y = random.randint(100, 1000)
            self.adb.run_adb_command(f"shell input tap {x} {y}")
            time.sleep(1)  # Пауза между кликами
        
        logging.info("Активность имитирована")