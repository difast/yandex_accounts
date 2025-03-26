Python – основной язык
ADB (Android Debug Bridge) – управление устройствами
Многопоточность (threading) – параллельная обработка аккаунтов
Логирование (logging) – запись событий
JSON – хранение конфигов и сессий ***
Git – контроль версий
Для визуализации:
Системные Android Intent (через adb shell am)
Ручное управление координатами тапов
Зависимости:
Только стандартные библиотеки Python (os, logging, threading и т.д.)



1. Установка ADB
1. Скачайть(https://developer.android.com/studio/releases/platform-tools)(если нет)
2. Распаковать архив

2. Добавьте путь к ADB в переменную окружения PATH:
На Windows:
     	1. Откройте gанель управления Win + R -- sysdm.cpl Ок -- Дополнительные → Переменные среды.
     	2. В разделе системные переменные найдите переменную `Path` и нажмите "Изменить".
     	3. Добавьте путь к папке `platform-tools`(которую распаковали после установки) (например, `C:\platform-tools`).


3. Проверьте, что ADB работает:
В терминале введите: adb --version
Отобразиться версия adb

4. Проверить root-доступ
команда: adb root
Должен у вас быть если устройство уже подключено, без него не получиться сохранять образы сессий


5. Переходим в папку проекта

6. Установка зависимостей
В целом как я уже говорил в коде уже встроенные библиотеки, но если понадобитья тестирование из файла test_session_saver.py то можно установить pytest:

В терминале: pip install pytest
Проверить, что pytest установился: pytest --version
Команда для запуска теста: python -m pytest tests/test_session_saver.py -v или python -m pytest tests/
 
7. Подготовка файла LogPass.txt
1. Откройте папку `data` в проекте.
2. В файле LogPass.txt нужно заполнить в формате: логин1:пароль1:прокси1:порт1:2FA_код1 (прокси1:порт1 это сервер то есть IP:Порт)
Можно добавить второй вариант еще: логин2:пароль2:прокси2:порт2:2FA_код2

8. Проверка доступности устройства по adb:
В терминале введите: adb devices
Должен быть ответ например:
  List of devices attached
  emulator-5554   device

  
9. Запуск программы
1. Нужно находится в папке проекта
2. Запустите программу: python main.py или python3 main.py (если несколько версий Python у вас)

10. Проверка логов в logs/app.log
