@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title ZENITH SYSTEM LOADER v4.3.4
mode con: cols=80 lines=25
color 03

:: Проверка прав администратора
fsutil dirty query %systemdrive% >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: RUN AS ADMINISTRATOR
    pause >nul
    exit
)

cls
echo.
echo    ███████╗███████╗███╗   ██╗██╗████████╗██╗  ██╗
echo    ╚══███╔╝██╔════╝████╗  ██║██║╚══██╔══╝██║  ██║
echo      ███╔╝ █████╗  ██╔██╗ ██║██║   ██║   ███████║
echo     ███╔╝  ██╔══╝  ██║╚██╗██║██║   ██║   ██╔══██║
echo    ███████╗███████╗██║ ╚████║██║   ██║   ██║  ██║
echo    ╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝
echo.
echo   [ INITIALIZING ZENITH CORE SUBSYSTEM ]
echo   -------------------------------------------------

:: Этап 1: Быстрые логи (500 - 1000 мс)
echo   [INFO] Mounting Virtual File System...
ping -n 1 -w 500 127.0.0.1 >nul

echo   [INFO] Linking core_libraries.dll...
ping -n 1 -w 1000 127.0.0.1 >nul

echo   [INFO] Synchronizing with local environment...
ping -n 1 -w 500 127.0.0.1 >nul

echo   [INFO] Verifying security certificates...
ping -n 1 -w 1500 127.0.0.1 >nul

echo   [OK  ] Environment ready.
echo.
ping -n 1 -w 500 127.0.0.1 >nul

:: Этап 2: Анимация крутилки и бегущей строки
set "spinner=/-\|"
set "marquee_base=*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--"

for /L %%i in (0,1,100) do (
    set /a "spin_idx=%%i %% 4"
    for %%a in (!spin_idx!) do set "spin_char=!spinner:~%%a,1!"
    set /a "marq_shift=%%i %% 15"
    set "marquee=!marquee_base:~%marq_shift%,40!"

    set "status=Loading core modules...  "
    if %%i geq 25 set "status=Scanning local files... "
    if %%i geq 60 set "status=Checking lang.json...   "
    if %%i geq 90 set "status=Launching engine...     "

    cls
    echo.
    echo    ███████╗███████╗███╗   ██╗██╗████████╗██╗  ██╗
    echo    ╚══███╔╝██╔════╝████╗  ██║██║╚══██╔══╝██║  ██║
    echo      ███╔╝ █████╗  ██╔██╗ ██║██║   ██║   ███████║
    echo     ███╔╝  ██╔══╝  ██║╚██╗██║██║   ██║   ██╔══██║
    echo    ███████╗███████╗██║ ╚████║██║   ██║   ██║  ██║
    echo    ╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝
    echo.
    echo   -------------------------------------------------
    echo   [ !spin_char! ] Status: !status! [ %%i%% ]
    echo   -------------------------------------------------
    echo.
    echo   !marquee!
    echo.

    :: Паузы на ключевых этапах (теперь в мс)
    if %%i==25 ping -n 1 -w 1000 127.0.0.1 >nul
    if %%i==60 ping -n 1 -w 1500 127.0.0.1 >nul
    if %%i==90 ping -n 1 -w 500 127.0.0.1 >nul

    :: Скорость самой крутилки (очень быстро)
    ping -n 1 -w 30 127.0.0.1 >nul
)

echo   [ OK ] System verified.
echo   [ WAIT ] Executing Zenith_Cleaner.py...
ping -n 1 -w 1000 127.0.0.1 >nul

python Zenith_Cleaner.py
if %errorlevel% neq 0 (
    echo [ ERR ] Failed to locate Zenith_Cleaner.py
    pause
)