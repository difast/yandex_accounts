# scripts/device_spoofer.py
class DeviceSpoofer:
    def __init__(self, adb_manager):
        self.adb = adb_manager

    def set_imei(self, new_imei):
        """Меняет IMEI через системный файл (требуется root)."""
        # Получаем доступ к радио-модулю
        self.adb.run_adb_command("shell su -c 'service call iphonesubinfo 1'")
        
        #Записываем новый IMEI
        cmd = f"shell su -c 'echo {new_imei} > /data/data/com.android.phone/files/imei.txt'"
        return self.adb.run_adb_command(cmd)

    def spoof_device(self, params):
        """Меняет несколько параметров устройства."""
        # Подмена MAC-адреса
        self.adb.run_adb_command(f"shell settings put secure android_id {params['android_id']}")
        self.adb.run_adb_command(f"shell svc wifi setmac {params['mac_address']}")