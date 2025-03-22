import subprocess
import logging

class ADBManager:
    def __init__(self, device_id):
        """Инициализирует менеджер ADB для работы с конкретным устройством."""
        self.device_id = device_id

    def run_adb_command(self, command):
        """Выполняет ADB-команду для конкретного устройства."""
        # Добавляем ID устройства к команде, если он указан
        if self.device_id:
            command = f"adb -s {self.device_id} {command}"
        else:
            command = f"adb {command}"
        
        try:
            # Выполняем команду
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8').strip()  # Возвращаем результат в виде строки
        except subprocess.CalledProcessError as e:
            # Логируем ошибку
            error_message = e.output.decode('utf-8').strip()
            logging.error(f"Ошибка ADB: {error_message}")
            return None

    def check_device_connection(self):
        """Проверяет, подключено ли устройство."""
        result = self.run_adb_command("devices")
        if self.device_id in result:
            return True
        return False

    def reboot_device(self):
        """Перезагружает устройство."""
        return self.run_adb_command("reboot")

    def pull_file(self, remote_path, local_path):
        """Копирует файл с устройства на компьютер."""
        return self.run_adb_command(f"pull {remote_path} {local_path}")

    def push_file(self, local_path, remote_path):
        """Копирует файл с компьютера на устройство."""
        return self.run_adb_command(f"push {local_path} {remote_path}")

    def install_apk(self, apk_path):
        """Устанавливает APK-файл на устройство."""
        return self.run_adb_command(f"install {apk_path}")

    def uninstall_apk(self, package_name):
        """Удаляет приложение с устройства по имени пакета."""
        return self.run_adb_command(f"uninstall {package_name}")

if __name__ == "__main__":
    # Пример использования
    device_id = "реальный_ID_устройства"  # Замените на реальный ID !!! узнать ID:    adb devices (Bash)
    adb = ADBManager(device_id)
    
    # Проверка подключения устройства
    if adb.check_device_connection():
        print(f"Устройство {device_id} подключено.")
        
        # Пример выполнения команды
        model = adb.run_adb_command("shell getprop ro.product.model")
        print(f"Модель устройства: {model}")
    else:
        print(f"Устройство {device_id} не подключено.")