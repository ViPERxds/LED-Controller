# 📦 Создание релиза на GitHub

## 🚀 Пошаговая инструкция:

### 1. Перейди на GitHub
Открой: https://github.com/ViPERxds/LED-Controller

### 2. Создай релиз
1. Нажми на **"Releases"** (справа от кода)
2. Нажми **"Create a new release"**
3. Заполни:
   - **Tag version**: `v1.0.0`
   - **Release title**: `LED Controller v1.0.0`
   - **Description**: 
     ```
     🎉 Первый релиз LED Controller!
     
     ✨ Возможности:
     - Современный интерфейс на CustomTkinter
     - Поддержка ELK-BLEDOM и других LED лент
     - Управление цветом и яркостью
     - Готовый EXE файл для Windows
     
     📥 Просто скачайте и запустите!
     ```

### 3. Загрузи EXE файл
1. В разделе **"Attach binaries"** перетащи файл:
   `C:\Users\lenovo\Desktop\lenata\dist\LED_Controller.exe`
2. Или нажми **"Choose your files"** и выбери EXE

### 4. Опубликуй релиз
1. Поставь галочку **"Set as the latest release"**
2. Нажми **"Publish release"**

## ✅ Результат:

После этого в README будет работать кнопка:
```markdown
[![Download EXE](https://img.shields.io/badge/Download-LED_Controller.exe-brightgreen?style=for-the-badge&logo=windows)](https://github.com/ViPERxds/LED-Controller/releases/latest/download/LED_Controller.exe)
```

Люди смогут скачивать EXE одним кликом! 🚀

## 🔄 Для обновлений:

1. Собери новый EXE: `build_exe.bat`
2. Создай новый релиз с версией `v1.1.0`
3. Загрузи новый EXE
4. Кнопка в README автоматически обновится!
