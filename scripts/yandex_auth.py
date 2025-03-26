import time
import logging
import random
import secrets

class YandexAuth:
    def __init__(self, adb_manager):
        self.adb = adb_manager
        self.current_password = None
        self.new_password = None
        self.logger = logging.getLogger('YandexAuth')

    def _show_visual(self, message):
        """Визуальное отображение действия на устройстве (без логирования)"""
        try:
            self.adb.run_adb_command(
                f"shell am start -a android.intent.action.VIEW "
                f"-d 'message://{message}'"
            )
            time.sleep(1)
        except Exception:
            pass

    def _log_action(self, message):
        """Только логирование без визуального отображения"""
        self.logger.info(message)

    def login_to_browser(self, login, password, twofa_code=None):
        """Авторизация в браузере с визуальным контролем"""
        try:
            # 1. Открытие браузера
            self._log_action("[1/5] Открытие Яндекс.Браузера")
            self._show_visual("Открытие браузера")
            self.adb.run_adb_command(
                "shell am start -n com.yandex.browser/.YandexBrowserActivity"
            )
            time.sleep(3)

            # 2. Ввод логина
            self._log_action("[2/5] Ввод логина")
            self._show_visual("Ввод логина")
            self.adb.run_adb_command("shell input tap 300 500")
            self.adb.run_adb_command(f"shell input text {login}")
            self.adb.run_adb_command("shell input keyevent 66")
            time.sleep(2)

            # 3. Ввод пароля
            self._log_action("[3/5] Ввод пароля")
            self._show_visual("Ввод пароля")
            self.adb.run_adb_command("shell input tap 300 600")
            self.adb.run_adb_command(f"shell input text {password}")
            self.adb.run_adb_command("shell input keyevent 66")
            time.sleep(2)

            # 4. 2FA при необходимости
            if twofa_code:
                self._log_action("[4/5] Ввод 2FA кода")
                self._show_visual("Ввод 2FA")
                self.adb.run_adb_command("shell input tap 300 700")
                self.adb.run_adb_command(f"shell input text {twofa_code}")
                self.adb.run_adb_command("shell input keyevent 66")
                time.sleep(2)

            self.current_password = password
            self._log_action("[5/5] Авторизация успешно завершена")
            return True

        except Exception as e:
            self._log_action(f"Ошибка авторизации: {str(e)}")
            return False

    def change_password_via_app(self, new_password):
        """Смена пароля с визуальным контролем"""
        try:
            self._log_action("[1/7] Открытие приложения Яндекс")
            self._show_visual("Открытие приложения")
            self.adb.run_adb_command(
                "shell am start -n ru.yandex.searchplugin/.MainActivity"
            )
            time.sleep(3)

            self._log_action("[2/7] Открытие меню")
            self._show_visual("Открытие меню")
            self.adb.run_adb_command("shell input tap 1000 100")
            time.sleep(1)
            
            self._log_action("[3/7] Переход в настройки")
            self._show_visual("Переход в настройки")
            self.adb.run_adb_command("shell input tap 500 800")
            time.sleep(1)
            
            self._log_action("[4/7] Выбор безопасности")
            self._show_visual("Меню безопасности")
            self.adb.run_adb_command("shell input tap 500 600")
            time.sleep(1)
            
            self._log_action("[5/7] Инициация смены пароля")
            self._show_visual("Смена пароля")
            self.adb.run_adb_command("shell input tap 500 700")
            time.sleep(2)

            self._log_action("[6/7] Ввод паролей")
            self._show_visual("Ввод старого пароля")
            self.adb.run_adb_command("shell input tap 300 500")
            self.adb.run_adb_command(f"shell input text {self.current_password}")
            time.sleep(1)
            
            self._show_visual("Ввод нового пароля")
            self.adb.run_adb_command("shell input tap 300 600")
            self.adb.run_adb_command(f"shell input text {new_password}")
            time.sleep(1)
            
            self._log_action("[7/7] Подтверждение смены пароля")
            self._show_visual("Подтверждение")
            self.adb.run_adb_command("shell input tap 300 700")
            time.sleep(5)
            
            self._log_action(f"Пароль успешно изменен на: {new_password}")
            return True

        except Exception as e:
            self._log_action(f"Ошибка смены пароля: {str(e)}")
            return False

    def generate_backup_codes_via_app(self):
        """Генерация резервных кодов"""
        try:
            self._log_action("[1/5] Открытие приложения")
            self._show_visual("Открытие приложения")
            self.adb.run_adb_command(
                "shell am start -n ru.yandex.searchplugin/.MainActivity"
            )
            time.sleep(2)
            
            self._log_action("[2/5] Открытие меню")
            self._show_visual("Открытие меню")
            self.adb.run_adb_command("shell input tap 1000 100")
            time.sleep(1)
            
            self._log_action("[3/5] Переход в настройки")
            self._show_visual("Переход в настройки")
            self.adb.run_adb_command("shell input tap 500 800")
            time.sleep(1)
            
            self._log_action("[4/5] Выбор безопасности")
            self._show_visual("Меню безопасности")
            self.adb.run_adb_command("shell input tap 500 600")
            time.sleep(1)
            
            self._log_action("[5/5] Генерация кодов")
            self._show_visual("Генерация кодов")
            self.adb.run_adb_command("shell input tap 500 400")
            time.sleep(2)
            
            self._log_action("Резервные коды успешно созданы")
            return True
            
        except Exception as e:
            self._log_action(f"Ошибка генерации кодов: {str(e)}")
            return False

    def login_to_taxi(self, login, password):
        """Авторизация в Яндекс.Такси"""
        try:
            self._log_action("[1/5] Открытие приложения Такси")
            self._show_visual("Открытие Такси")
            self.adb.run_adb_command(
                "shell am start -n ru.yandex.taxi/.MainActivity"
            )
            time.sleep(2)
            
            self._log_action("[2/5] Нажатие кнопки Войти")
            self._show_visual("Нажатие Войти")
            self.adb.run_adb_command("shell input tap 300 500")
            time.sleep(1)
            
            self._log_action("[3/5] Ввод логина")
            self._show_visual("Ввод логина")
            self.adb.run_adb_command("shell input tap 300 600")
            self.adb.run_adb_command(f"shell input text {login}")
            time.sleep(1)
            
            self._log_action("[4/5] Ввод пароля")
            self._show_visual("Ввод пароля")
            self.adb.run_adb_command("shell input tap 300 700")
            self.adb.run_adb_command(f"shell input text {password}")
            time.sleep(1)
            
            self._log_action("[5/5] Подтверждение входа")
            self._show_visual("Подтверждение")
            self.adb.run_adb_command("shell input tap 300 800")
            time.sleep(3)
            
            self._log_action("Успешная авторизация в Яндекс.Такси")
            return True
            
        except Exception as e:
            self._log_action(f"Ошибка авторизации в Такси: {str(e)}")
            return False

    def simulate_activity(self):
        """Имитация активности пользователя"""
        try:
            self._log_action("Начало имитации активности")
            for i in range(5):
                x = random.randint(100, 900)
                y = random.randint(100, 1800)
                self._show_visual(f"Активность {i+1}/5")
                self.adb.run_adb_command(f"shell input tap {x} {y}")
                time.sleep(1)
            
            self._log_action("Имитация активности завершена")
            return True
            
        except Exception as e:
            self._log_action(f"Ошибка имитации активности: {str(e)}")
            return False