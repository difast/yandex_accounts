# utils/session_saver.py
import tarfile
import time
import logging
import os

def save_session(adb_manager, account_id):
    """Сохраняет только ключевые данные для восстановления сессии."""
    try:
        # Путь к данным Яндекс.Браузера на устройстве
        app_data_path = "/data/data/com.yandex.browser"  # Основная папка с данными
        
        # Ключевые файлы для сохранения
        key_files = [
            "app_webview/Cookies",          # Куки
            "app_webview/Local Storage",     # Локальное хранилище
            "shared_prefs/com.yandex.browser_preferences.xml"  # Настройки
        ]
        
        # Создаем временный архив на устройстве
        timestamp = int(time.time())
        temp_archive = f"/sdcard/session_temp_{timestamp}.tar.gz"
        
        # Архивируем только ключевые файлы
        for file in key_files:
            adb_manager.run_adb_command(f"shell su -c 'tar -czf {temp_archive} -C {app_data_path} {file}'")
        
        # Копируем архив на компьютер
        archive_name = f"data/sessions/session_{account_id}_{timestamp}.tar.gz"
        
        # Убедимся, что папка data/sessions существует
        os.makedirs("data/sessions", exist_ok=True)
        
        # Выполняем команду pull
        adb_manager.run_adb_command(f"pull {temp_archive} {archive_name}")
        
        # Удаляем временный архив с устройства
        adb_manager.run_adb_command(f"shell rm {temp_archive}")
        
        logging.info(f"Сессия сохранена: {archive_name}")
        return archive_name
    except Exception as e:
        logging.error(f"Ошибка сохранения сессии: {e}")
        return None
    
