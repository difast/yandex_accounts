# tests/test_session_saver.py
import sys
import os
from unittest import TestCase

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.session_saver import save_session
from tests.mock_adb import MockADBManager

class TestSessionSaver(TestCase):
    def test_save_session(self):
        """Тест для функции save_session."""
        adb_mock = MockADBManager("emulator-5554")
        
        result = save_session(adb_mock, "test_user")
        
        print("Лог команд:", adb_mock.commands_log)
        print("Результат функции:", result)
        
        self.assertIn("tar -czf", adb_mock.commands_log[0])
        self.assertIn("tar -czf", adb_mock.commands_log[1])
        self.assertIn("tar -czf", adb_mock.commands_log[2])
        self.assertIn("pull", adb_mock.commands_log[3])
        self.assertIn("rm", adb_mock.commands_log[4])
        
        self.assertIsNotNone(result)
        self.assertTrue(result.endswith(".tar.gz"))

# python -m pytest tests/test_session_saver.py -v