# 💡 LED Controller

Современное приложение для управления светодиодными лентами через Bluetooth на Windows.

![LED Controller](https://img.shields.io/badge/Platform-Windows-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Быстрый старт

### 📥 Скачать готовое приложение

[![Download EXE](https://img.shields.io/badge/Download-LED_Controller.exe-brightgreen?style=for-the-badge&logo=windows)](https://github.com/ViPERxds/LED-Controller/releases/latest/download/LED_Controller.exe)

**Просто скачайте и запустите!** Никаких дополнительных установок не требуется.

---

## ✨ Возможности

- 🔍 **Автоматическое сканирование** Bluetooth устройств
- 🎨 **Интерактивный выбор цвета** с RGB слайдерами
- 🌈 **Быстрые пресеты** популярных цветов
- 💡 **Управление яркостью** от 0 до 100%
- ⚡ **Включение/выключение** ленты
- 🖥️ **Современный интерфейс** на CustomTkinter
- 📱 **Поддержка ELK-BLEDOM** и других LED лент

## 🎯 Поддерживаемые устройства

- **ELK-BLEDOM** (основная поддержка)
- Magic Home LED strips
- Govee LED устройства
- Triones/TrLife контроллеры
- И другие BLE LED ленты

## 📖 Как использовать

### 1. Подключение
1. Включите LED ленту
2. Нажмите **"Сканировать"** в приложении
3. Выберите вашу ленту из списка (кликните на неё)
4. Нажмите **"Подключить"**

### 2. Управление цветом
- **RGB слайдеры** - точная настройка
- **Быстрые пресеты** - 8 популярных цветов
- **Палитра** - выбор любого цвета
- **Превью** - видите цвет в реальном времени

### 3. Управление яркостью
- Используйте слайдер **"Яркость"**
- Диапазон: 0% (выкл) - 100% (максимум)

## 🔧 Для разработчиков

### Установка из исходников

```bash
# Клонируйте репозиторий
git clone https://github.com/ViPERxds/LED-Controller.git
cd LED-Controller

# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
python led_controller.py
```

### Сборка EXE

```bash
# Установите PyInstaller
pip install pyinstaller

# Соберите EXE
pyinstaller --onefile --windowed --name "LED_Controller" led_controller.py
```

## 📋 Системные требования

- **ОС**: Windows 10/11 (x64)
- **Bluetooth**: 4.0 (BLE) или выше
- **RAM**: 50 MB
- **Место на диске**: 25 MB

## 🐛 Устранение неполадок

### Лента не подключается
1. Убедитесь что лента включена и в режиме сопряжения
2. Проверьте что Bluetooth включен на компьютере
3. Попробуйте перезапустить ленту
4. Убедитесь что лента не подключена к телефону

### Приложение не запускается
1. Убедитесь что у вас Windows 10/11
2. Попробуйте запустить от имени администратора
3. Проверьте что антивирус не блокирует файл

### Цвета не меняются
1. Проверьте подключение (статус должен быть "Подключено ✓")
2. Убедитесь что лента включена
3. Попробуйте переподключиться

## 📁 Структура проекта

```
LED-Controller/
├── led_controller.py      # Основное приложение
├── led_protocols.py       # Протоколы для разных лент
├── requirements.txt       # Зависимости Python
├── build_exe.bat         # Скрипт сборки EXE
├── BUILD_README.md       # Инструкция по сборке
├── TROUBLESHOOTING.md    # Решение проблем
└── dist/
    └── LED_Controller.exe # Готовое приложение
```

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! 

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📜 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

## 🙏 Благодарности

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - за красивый UI
- [Bleak](https://github.com/hbldh/bleak) - за работу с Bluetooth
- Сообществу разработчиков Python

## 📞 Поддержка

Если у вас возникли проблемы:

1. Проверьте раздел [Устранение неполадок](#-устранение-неполадок)
2. Создайте [Issue](https://github.com/ViPERxds/LED-Controller/issues)
3. Опишите проблему подробно

---

**Наслаждайтесь управлением вашей LED лентой! 🌈**

[![GitHub stars](https://img.shields.io/github/stars/ViPERxds/LED-Controller?style=social)](https://github.com/ViPERxds/LED-Controller)
[![GitHub forks](https://img.shields.io/github/forks/ViPERxds/LED-Controller?style=social)](https://github.com/ViPERxds/LED-Controller)