@echo off
chcp 65001 >nul
title Сборка LED Controller в EXE
echo ========================================
echo   Сборка LED Controller в EXE
echo ========================================
echo.

REM Проверка установки PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [!] PyInstaller не установлен
    echo Установка PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось установить PyInstaller
        pause
        exit /b 1
    )
)

echo [OK] PyInstaller найден
echo.

REM Удаление старых файлов сборки
if exist "dist" (
    echo Удаление старой сборки...
    rmdir /s /q dist
)

if exist "build" (
    rmdir /s /q build
)

if exist "*.spec" (
    del /q *.spec
)

echo.
echo ========================================
echo   Начало сборки...
echo ========================================
echo.

REM Сборка в один EXE файл
pyinstaller --onefile ^
    --windowed ^
    --name "LED_Controller" ^
    --icon=NONE ^
    --add-data "requirements.txt;." ^
    led_controller.py

if errorlevel 1 (
    echo.
    echo [ОШИБКА] Сборка не удалась
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Сборка завершена успешно!
echo ========================================
echo.
echo EXE файл находится в папке: dist\LED_Controller.exe
echo.
pause

