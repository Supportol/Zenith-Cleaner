@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title ZENITH LOADER

:: Проверка прав
fsutil dirty query %systemdrive% >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: RUN AS ADMINISTRATOR
    pause & exit
)

:: Чтение версии для заголовка
set "VER=6.1.3"
if exist "version.txt" (
    set /p VER=<version.txt
)

title ZENITH SYSTEM LOADER v!VER!

:: Запуск
python Zenith_Cleaner.py
if %errorlevel% neq 0 (
    echo [!] Zenith closed with error.
    pause
)
exit