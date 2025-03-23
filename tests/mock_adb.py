# tests/mock_adb.py
class MockADBManager:
    def __init__(self, device_id):
        """Инициализация мок-объекта для ADBManager."""
        self.device_id = device_id
        self.commands_log = []

    def run_adb_command(self, command):
        """Мок-метод для выполнения ADB-команды."""
        self.commands_log.append(command)
        
        # успешное выполнение команды
        if "pull" in command:
            return "File pulled successfully"
        elif "push" in command:
            return "File pushed successfully"
        return "Mocked success response"

    def check_device_connection(self):
        """Мок-метод для проверки подключения устройства."""
        return True