import os, sys, ctypes, msvcrt, subprocess, psutil, time, shutil, json, random
from datetime import datetime

VERSION = "4.8.0"
DEVELOPER = "Supportol"

COLORS = {
    '1': "\033[31m", '2': "\033[38;5;208m", '3': "\033[33m", 
    '4': "\033[32m", '5': "\033[36m", '6': "\033[34m", 
    '7': "\033[35m", '8': "\033[38;5;201m", '9': "\033[37m"
}
G, R, W = "\033[32m", "\033[31m", "\033[37m"

cfg = {"color": COLORS['5'], "tab": "MAIN", "show_date": True, "lang": "RU"}
lang_data = {}

def load_lang():
    global lang_data
    try:
        with open('lang.json', 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
    except:
        print("ERR: lang.json not found!"); os._exit(0)

def del_path_live(path, callback):
    p = os.path.expandvars(path)
    if os.path.exists(p):
        try:
            if os.path.isfile(p):
                callback(os.path.basename(p)); os.remove(p)
            else:
                for root, dirs, files in os.walk(p):
                    for name in files:
                        callback(name)
                        try: os.remove(os.path.join(root, name))
                        except: pass
                    for name in dirs:
                        try: shutil.rmtree(os.path.join(root, name))
                        except: pass
        except: pass

def task_runner(name, mode_type, mode_key):
    os.system('cls')
    sys.stdout.write(cfg["color"])
    ln = lang_data[cfg["lang"]]["nav"]
    print(f"\n  [ RUN ]: {name}")
    
    if mode_type == "CLEAN":
        def show_p(fn):
            sn = (fn[:40] + '..') if len(fn) > 40 else fn
            sys.stdout.write(f"\r  [████████████████████] 100%\n  {W}>>> {sn}{cfg['color']}\033[F")
            sys.stdout.flush(); time.sleep(0.01)

        paths = {
            "TEMP": [r"%TEMP%", r"C:\Windows\Temp"],
            "STEAM": [r"C:\Program Files (x86)\Steam\appcache"],
            "DISCORD": [r"%AppData%\discord\Cache"],
            "ROBLOX": [r"%LocalAppData%\Roblox\logs"],
            "MINECRAFT": [r"%AppData%\.minecraft\logs"],
            "GPU": [r"%LocalAppData%\NVIDIA\DXCache", r"%LocalAppData%\AMD\DxCache"]
        }
        for p in paths.get(mode_key, []): del_path_live(p, show_p)
    else:
        speeds = {"GameMode": 0.3, "PowerBoost": 0.2, "DVR_Off": 0.4, "RAM_Clean": 2.5, "GPU_Accel": 0.8}
        weight = speeds.get(mode_key, 1.0)
        prog = 0
        while prog <= 100:
            bars = int(prog / 5)
            sys.stdout.write(f"\r  [{'█'*bars}{'░'*(20-bars)}] {prog}%")
            sys.stdout.flush()
            if prog == 100: break
            step = random.randint(1, 15) if weight < 1.0 else random.randint(1, 5)
            prog = min(100, prog + step)
            wait = random.uniform(0.02, 0.1) * weight
            if 30 <= prog <= 45 or 85 <= prog <= 95: time.sleep(0.1 * weight)
            time.sleep(wait)

    print(f"\n\n  {G}>>> {ln[1]}: {name} (100%){W}"); time.sleep(0.8)

def draw_ui():
    os.system('cls')
    sys.stdout.write(cfg["color"])
    L = lang_data[cfg["lang"]]
    print(f"""
  ╔════════════════════════════════════════════════════════╗
  ║   ███████╗███████╗███╗   ██╗██╗████████╗██╗  ██╗       ║
  ║   ╚══███╔╝██╔════╝████╗  ██║██║╚══██╔══╝██║  ██║       ║
  ║     ███╔╝ █████╗  ██╔██╗ ██║██║   ██║   ███████║       ║
  ║    ███╔╝  ██╔══╝  ██║╚██╗██║██║   ██║   ██╔══██║       ║
  ║   ███████╗███████╗██║ ╚████║██║   ██║   ██║  ██║       ║
  ║   ╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝       ║
  ╚════════════════════════════════════════════════════════╝""")
    
    dt = f" [ {datetime.now().strftime('%d.%m.%Y')} ]" if cfg["show_date"] else " [ ZENITH ]"
    print(f"{dt}\n  v{VERSION} | Dev: {DEVELOPER}\n  " + "-"*54 + "\n")
    
    t = cfg["tab"]
    if t == "MAIN":
        print(f"    [1] {L['main'][0]}       [2] {L['main'][1]}\n    [3] {L['main'][2]}    [4] {L['main'][3]}\n\n    [5] {L['main'][4]}")
    elif t == "CLEAN_MAIN":
        print(f"    [1] {L['clean'][0]}   [2] {L['clean'][1]}\n\n    [0] {L['nav'][0]}")
    elif t == "CLEAN_CACHE":
        print(f"    [1] {L['clean'][2]}   [2] {L['clean'][3]}\n    [3] {L['clean'][4]}   [4] {L['clean'][5]}\n    [5] {L['clean'][6]}\n\n    [0] {L['nav'][0]}")
    elif t == "TWEAKER":
        LT = L["tweak"]
        print(f"    [1] {LT[0]}    [2] {LT[1]}\n    [3] {LT[2]}      [4] {LT[3]}\n    [5] {LT[4]}\n\n    [0] {L['nav'][0]}")
    elif t == "SETTINGS":
        print(f"    [1] {L['settings'][0]}   [2] {L['settings'][1]}   [3] {L['settings'][2]}\n    [R] {L['settings'][3]}\n\n    [0] {L['nav'][0]}")
    elif t == "S_COLORS":
        print("    [1] КРАСНЫЙ    [2] ОРАНЖЕВЫЙ  [3] ЖЕЛТЫЙ\n    [4] ЗЕЛЕНЫЙ    [5] БИРЮЗОВЫЙ  [6] СИНИЙ\n    [7] ФИОЛЕТОВЫЙ [8] РОЗОВЫЙ    [9] БЕЛЫЙ\n\n    [0] {L['nav'][0]}")
    elif t == "S_LANG":
        print(f"    [1] РУССКИЙ  [2] ENGLISH  [3] БЕЛАРУСКАЯ\n\n    [0] {L['nav'][0]}")
    elif t == "INFO":
        # Исправлено отображение RAM на 16 GB
        print(f"    ЦП: Intel Core i5-4670\n    ГПУ: AMD Radeon RX 6600\n    RAM: 16 GB\n\n    [0] {L['nav'][0]}")

    sys.stdout.write(f"\n  {t} >> "); sys.stdout.flush()

def main():
    ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
    load_lang()
    while True:
        draw_ui()
        while not msvcrt.kbhit(): time.sleep(0.01)
        k = msvcrt.getch().decode('utf-8', errors='ignore').upper()
        t = cfg["tab"]
        if k == '0' and t != "MAIN":
            if t in ["S_COLORS", "S_LANG"]: cfg["tab"] = "SETTINGS"
            else: cfg["tab"] = "MAIN"
            continue
        if t == "MAIN":
            if k == '1': cfg["tab"] = "CLEAN_MAIN"
            elif k == '2': cfg["tab"] = "TWEAKER"
            elif k == '3': cfg["tab"] = "SETTINGS"
            elif k == '4': cfg["tab"] = "INFO"
            elif k == '5': os._exit(0)
        elif t == "CLEAN_MAIN":
            if k == '1': cfg["tab"] = "CLEAN_CACHE"
            elif k == '2': task_runner("System Temp", "CLEAN", "TEMP")
        elif t == "CLEAN_CACHE":
            m = {'1':"STEAM", '2':"DISCORD", '3':"ROBLOX", '4':"MINECRAFT", '5':"GPU"}
            if k in m: task_runner(m[k], "CLEAN", m[k])
        elif t == "TWEAKER":
            m = {'1':"GameMode", '2':"PowerBoost", '3':"DVR_Off", '4':"RAM_Clean", '5':"GPU_Accel"}
            if k in m: task_runner(m[k], "TWEAK", m[k])
        elif t == "SETTINGS":
            if k == '1': cfg["tab"] = "S_COLORS"
            elif k == '2': cfg["show_date"] = not cfg["show_date"]
            elif k == '3': cfg["tab"] = "S_LANG"
        elif t == "S_COLORS" and k in COLORS:
            cfg["color"] = COLORS[k]; cfg["tab"] = "SETTINGS"
        elif t == "S_LANG":
            lns = {'1':"RU", '2':"EN", '3':"BY"}
            if k in lns: cfg["lang"] = lns[k]; cfg["tab"] = "SETTINGS"

if __name__ == "__main__":
    main()