import os
import logging
import threading
from scripts.adb_manager import ADBManager
from scripts.yandex_auth import YandexAuth
from utils.file_parser import parse_logpass
from utils.session_saver import save_session


# Настройка логирования
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"  # Кодировку UTF-8
)
logging.info("Программа запущена")

# Создание папок, если их нет
os.makedirs("data/sessions", exist_ok=True)
os.makedirs("logs", exist_ok=True)

def process_account(device_id, account):
    """Обрабатывает один аккаунт на одном устройстве."""
    adb = ADBManager(device_id)

    # Проверка подключения устройства
    if not adb.check_device_connection():
        logging.error(f"Устройство {device_id} не подключено. Пропуск аккаунта {account['login']}.")
        return  # Прерываем выполнение для этого аккаунта
    auth = YandexAuth(adb)
    
    # Авторизация в Яндекс.Браузере
    auth.login_to_browser(account['login'], account['password'], account['2fa_code'])
    
    # Смена пароля через приложение
    auth.change_password_via_app("NewPassword123")
    
    # Создание резервных кодов через приложение
    auth.generate_backup_codes_via_app()
    
    # Авторизация в Яндекс.Такси
    auth.login_to_taxi(account['login'], account['password'])
    
    # Имитация активности
    auth.simulate_activity()
    
    # Сохранение сессии
    session_path = save_session(adb, account['login'])
    if session_path:
        logging.info(f"Сессия сохранена: {session_path}")
    else:
        logging.error("Ошибка сохранения сессии")

# Чтение аккаунтов
accounts = parse_logpass("data/LogPass.txt")

# Запуск потоков
threads = []
for i, account in enumerate(accounts):
    device_id = "реальный_ID_устройства"  # Замените на реальный ID устройства
    thread = threading.Thread(target=process_account, args=(device_id, account))
    threads.append(thread)
    thread.start()

# Ожидание завершения всех потоков
for thread in threads:
    thread.join()

logging.info("Программа завершена")




#result = adb.run_adb_command("shell getprop ro.product.model")
#print(result)  # Должна отобразиться модель устройства