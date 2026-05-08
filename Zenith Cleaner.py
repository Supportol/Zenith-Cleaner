import os
import shutil
import subprocess
import time
import psutil
import sys
import ctypes
import math
import requests

# === КОНФИГУРАЦИЯ ===
VERSION = "1.5.0"
DEVELOPER = "Supportol"
# Ссылка настроена на твой ник. Когда создашь репозиторий 'Zenith-Cleaner', апдейтер заработает.
RAW_CODE_URL = "https://cdn.jsdelivr.net/gh/Supportol/Zenith-Cleaner@main/cleaner.py"

# --- РАДУЖНЫЙ ИНТЕРФЕЙС ---

def get_gradient_color(x, y, width, height, shift=0):
    position = (x / width + y / height) / 2 + shift
    r = int(127 * (math.sin(position * math.pi * 2) + 1))
    g = int(127 * (math.sin(position * math.pi * 2 + 2 * math.pi / 3) + 1))
    b = int(127 * (math.sin(position * math.pi * 2 + 4 * math.pi / 3) + 1))
    return f"\033[38;2;{r};{g};{b}m"

def print_rainbow_logo(shift=0):
    lines = [
        "    Z E N I T H   C L E A N E R",
        "    ════════════════════════════════════════════════════════════",
        "      ███████╗ ███████╗ ███╗   ██╗ ██╗ ████████╗ ██╗  ██████╗ ",
        "      ╚══███╔╝ ██╔════╝ ████╗  ██║ ██║ ╚══██╔══╝ ██║ ██╔════╝ ",
        "        ███╔╝  █████╗   ██╔██╗ ██║ ██║    ██║    ██║ ██║      ",
        "       ███╔╝   ██╔══╝   ██║╚██╗██║ ██║    ██║    ██║ ██║      ",
        "      ███████╗ ███████╗ ██║ ╚████║ ██║    ██║    ██║ ╚██████╗ ",
        "      ╚══════╝ ╚══════╝ ╚═╝  ╚═══╝ ╚═╝    ╚═╝    ╚═╝  ╚═════╝ ",
        "    ════════════════════════════════════════════════════════════"
    ]
    height = len(lines)
    max_width = max(len(line) for line in lines)
    output = ""
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            output += get_gradient_color(x, y, max_width, height, shift) + char
        output += "\033[0m\n"
    sys.stdout.write(output)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- СИСТЕМНАЯ ЛОГИКА ---

def auto_update():
    """Проверка обновлений через jsDelivr (зеркало GitHub)"""
    try:
        response = requests.get(RAW_CODE_URL, timeout=5)
        if response.status_code == 200:
            new_code = response.text
            if f'VERSION = "{VERSION}"' not in new_code:
                print(f"\n\033[93m[!] Доступна новая версия! Начинаю обновление...\033[0m")
                with open(__file__, "w", encoding="utf-8") as f:
                    f.write(new_code)
                print("\033[92m[OK] Zenith Cleaner обновлен. Перезапустите программу!\033[0m")
                input("Нажмите Enter для выхода...")
                sys.exit()
    except:
        pass # Игнорируем ошибки сети, чтобы дать запустить программу офлайн

def kill_everything():
    """Закрытие игровых процессов и лаунчеров"""
    targets = [
        "steam.exe", "discord.exe", "telegram.exe", "chrome.exe", "FL64.exe",
        "wot.exe", "WorldOfTanks.exe", "lgc.exe", "LestaGameCenter.exe",
        "cs2.exe", "javaw.exe", "RDR2.exe", "RobloxPlayerBeta.exe", "SonsOfTheForest.exe"
    ]
    for app in targets:
        subprocess.run(f"taskkill /f /im {app} /t", shell=True, capture_output=True)

def run_cleaning():
    clear_console()
    print_rainbow_logo()
    print(f"\n\033[94m[*] Выполнение протоколов очистки Supportol...\033[0m")
    
    kill_everything()
    
    local = os.environ.get('LocalAppData', '')
    roaming = os.environ.get('AppData', '')
    
    tasks = {
        "Временные файлы": os.environ.get('TEMP'),
        "Кеш шейдеров AMD": os.path.join(local, r"AMD\DxCache"),
        "Кеш шейдеров DX": os.path.join(local, "D3DSCache"),
        "Кеш Мира Танков": os.path.join(roaming, r"Wargaming.net\WorldOfTanks\web_cache"),
        "Кеш Steam": os.path.join(local, r"Steam\htmlcache"),
        "Сброс DNS": "ipconfig /flushdns"
    }

    for name, path in tasks.items():
        print(f"  \033[96m>>\033[0m Обработка: {name}")
        if "/" in path or " " in path: # Если это команда
            subprocess.run(path, shell=True, capture_output=True)
        elif os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
            os.makedirs(path, exist_ok=True)
        time.sleep(0.3)

    print(f"\n\033[92m[SUCCESS] Очистка завершена. Система готова к игре!\033[0m")
    input("\nНажмите Enter...")

# --- ГЛАВНОЕ МЕНЮ ---

def main():
    # Настройка цветов для Windows
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    
    # 1. Проверка обновлений
    auto_update()
    
    while True:
        clear_console()
        # Логотип плавно переливается в реальном времени
        print_rainbow_logo(shift=time.time() * 0.4)
        
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        
        print(f" \033[1m>> CPU: {cpu}% | RAM: {ram}% | Dev: {DEVELOPER}\033[0m\n")
        print(f" \033[92m[1]\033[0m ЗАПУСТИТЬ ОЧИСТКУ")
        print(f" \033[92m[2]\033[0m ИНФОРМАЦИЯ")
        print(f" \033[91m[3]\033[0m ВЫХОД")
        
        choice = input(f"\n\033[96mZenith_Console > \033[0m")
        
        if choice == '1':
            run_cleaning()
        elif choice == '2':
            clear_console()
            print_rainbow_logo()
            print(f"\n\033[1mZENITH CLEANER v{VERSION}\033[0m")
            print(f"Автор: {DEVELOPER}")
            print("Скрипт создан для оптимизации ПК под тяжелые игры и софт.")
            print("Включает глубокую очистку DxCache для видеокарт AMD.")
            input("\nНазад [Enter]...")
        elif choice == '3':
            sys.exit()

if __name__ == "__main__":
    main()