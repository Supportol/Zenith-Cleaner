import os, sys, ctypes, subprocess, psutil, time, platform, glob, json, shutil

VERSION = "7.0.0"

COLORS = {
    '1': "\033[34m", '2': "\033[32m", '3': "\033[36m", '4': "\033[31m",
    '5': "\033[35m", '6': "\033[33m", '7': "\033[37m", '8': "\033[90m",
    '9': "\033[94m", '10': "\033[92m", '11': "\033[96m", '12': "\033[91m",
    '13': "\033[95m", '14': "\033[93m", '15': "\033[97m",
    '16': "\033[38;5;208m", '17': "\033[38;5;190m", '18': "\033[38;5;45m",
    '19': "\033[38;5;201m", '20': "\033[38;5;46m"
}

cfg = {"color_key": '7', "lang": "EN", "tab": "MAIN"}
lang_data = {}

def save_cfg():
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump({"color_key": cfg["color_key"], "lang": cfg["lang"]}, f)

def load_cfg():
    global cfg
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                cfg.update(json.load(f))
        except: save_cfg()
    else: save_cfg()

def load_res():
    global lang_data
    if os.path.exists('lang.json'):
        with open('lang.json', 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
    else:
        print("FATAL ERROR: lang.json missing!"); time.sleep(3); sys.exit()

def get_hw():
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        cpu = winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
    except: cpu = platform.processor()
    return cpu, f"{round(psutil.virtual_memory().total / (1024**3))} GB"

def smart_action(name, paths=None, cmd=None):
    os.system('cls')
    sys.stdout.write(COLORS.get(cfg["color_key"], "\033[37m"))
    L = lang_data[cfg["lang"]]
    print(f"\n  ║ {L['ui']['process']}: {name}")
    print("  ╚" + "═"*55)
    
    if paths:
        files = []
        for p in paths:
            expanded = os.path.expandvars(p)
            files.extend(glob.glob(os.path.join(expanded, '*')))
            files.extend(glob.glob(os.path.join(expanded, '.*')))
            
        if not files: 
            print(f"\n  >>> {L['ui']['already_clean']}"); time.sleep(0.8); return
            
        total = len(files)
        for i, f in enumerate(files):
            try:
                if os.path.isfile(f) or os.path.islink(f): os.unlink(f)
                elif os.path.isdir(f): shutil.rmtree(f)
                p_v = int((i+1)/total*100)
                sys.stdout.write(f"\r  [{'█'*(p_v//5)}{' '*(20-(p_v//5))}] {p_v}% | {os.path.basename(f)[:20]}")
                sys.stdout.flush()
            except: continue
            
    if cmd:
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for i in range(1, 11):
            sys.stdout.write(f"\r  {L['ui']['working']}: [{'#'*i}{'-'*(10-i)}] {i*10}%")
            sys.stdout.flush(); time.sleep(0.03)

    print(f"\n\n  >>> {L['ui']['done']}!"); time.sleep(0.7)

def draw_ui():
    os.system('cls')
    sys.stdout.write(COLORS.get(cfg["color_key"], "\033[37m"))
    L = lang_data[cfg["lang"]]
    print(r"""
  ╔════════════════════════════════════════════════╗
  ║  ███████╗███████╗███╗   ██╗██╗████████╗██╗  ██╗║
  ║  ╚══███╔╝██╔════╝████╗  ██║██║╚══██╔══╝██║  ██║║
  ║    ███╔╝ █████╗  ██╔██╗ ██║██║   ██║   ███████║║
  │   ███╔╝  ██╔══╝  ██║╚██╗██║██║   ██║   ██╔══██║│
  ║  ███████╗███████╗██║ ╚████║██║   ██║   ██║  ██║║
  ║  ╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝║
  ╚════════════════════════════════════════════════╝""")
    print(f"  ZENITH PROJECT | v{VERSION} | {L['ui']['lang_tag']}: {cfg['lang']}")
    print("  " + "─"*50)
    
    t = cfg["tab"]
    if t == "MAIN":
        for i, m in enumerate(L["main"], 1): print(f"  [{i}] {m}")
        print(f"\n  [0] {L['ui']['exit']}")
    elif t == "CLEAN":
        for i, name in enumerate(L["clean"], 1):
            print(f"  [{str(i).zfill(2)}] {name.ljust(20)}", end="\n" if i % 2 == 0 else "")
        print(f"\n  [0] {L['ui']['back']}")
    elif t == "TWEAK":
        for i, name in enumerate(L["tweak"], 1):
            print(f"  [{str(i).zfill(2)}] {name.ljust(20)}", end="\n" if i % 2 == 0 else "")
        print(f"\n  [0] {L['ui']['back']}")
    elif t == "SET":
        print(f"  [100] {L['ui']['change_lang']} ({cfg['lang']})")
        for i in range(10):
            c1, v1 = L["colors"][i], str(i+1)
            c2, v2 = L["colors"][i+10], str(i+11)
            print(f"  {c1.ljust(12)} [{v1.zfill(2)}]  │  {c2.ljust(12)} [{v2}]")
        print(f"\n  [0] {L['ui']['back']}")
    elif t == "INFO":
        cpu, ram = get_hw()
        print(f"  CPU: {cpu}\n  RAM: {ram}\n\n  [0] {L['ui']['back']}")

    sys.stdout.write(f"\n  {t} >> "); sys.stdout.flush()

def main():
    load_cfg()
    load_res()
    try:
        with open("version.txt", "w", encoding="utf-8") as f: f.write(VERSION)
    except: pass
    if os.name == 'nt': ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
    
    while True:
        draw_ui()
        cmd_in = input().upper().strip()
        
        if cmd_in == '0' or cmd_in == '00':
            if cfg["tab"] == "MAIN": sys.exit()
            else: cfg["tab"] = "MAIN"; continue

        if cfg["tab"] == "MAIN":
            tabs = {'1':"CLEAN", '2':"TWEAK", '3':"SET", '4':"INFO"}
            if cmd_in in tabs: cfg["tab"] = tabs[cmd_in]
        
        elif cfg["tab"] == "SET":
            if cmd_in == '100':
                cfg["lang"] = "RU" if cfg["lang"] == "EN" else "EN"; save_cfg()
            elif cmd_in in COLORS:
                cfg["color_key"] = cmd_in; save_cfg()

        elif cfg["tab"] == "CLEAN":
            actions = {
                '1': (["%TEMP%", "C:\\Windows\\Temp"], None),
                '2': (None, "ipconfig /flushdns"),
                '3': (["C:\\$Recycle.Bin"], None),
                '4': (["C:\\Windows\\Prefetch"], None),
                '5': (["C:\\Windows\\Logs", "C:\\Windows\\System32\\winevt\\Logs"], None),
                '6': (["%LocalAppData%\\NVIDIA\\DXCache", "%LocalAppData%\\AMD\\DxCache"], None),
                '7': (["%LocalAppData%\\Google\\Chrome\\User Data\\Default\\Cache"], None),
                '8': (None, "net stop wuauserv && del /f /s /q %systemroot%\\SoftwareDistribution\\* && net start wuauserv"),
                '9': (["%LocalAppData%\\Microsoft\\Windows\\Explorer\\thumbcache_*.db"], None),
                '10': (["%AppData%\\Microsoft\\Windows\\Recent"], None),
                '11': (None, "wsreset.exe"),
                '12': (["%LocalAppData%\\Microsoft\\Windows\\WER"], None),
                '13': (["%LocalAppData%\\DirectX Shader Cache"], None),
                '14': (["C:\\Program Files (x86)\\Steam\\appcache", "C:\\Program Files (x86)\\Steam\\depotcache"], None),
                '15': (["%AppData%\\discord\\Cache", "%AppData%\\discord\\Code Cache"], None),
                '16': (["%LocalAppData%\\Spotify\\Storage"], None),
                '17': (["C:\\Windows\\ServiceProfiles\\NetworkService\\AppData\\Local\\Microsoft\\Windows\\DeliveryOptimization\\Cache"], None),
                '18': (None, "netsh branchcache flush"),
                '19': (None, "powershell -Command \"Remove-Item 'C:\\ProgramData\\Microsoft\\Windows Defender\\Scans\\History\\Service\\*' -Recurse\""),
                '20': (["%TEMP%", "C:\\Windows\\Temp", "C:\\Windows\\Prefetch", "C:\\$Recycle.Bin"], "ipconfig /flushdns")
            }
            if cmd_in in actions:
                p, c = actions[cmd_in]
                smart_action(lang_data[cfg["lang"]]["clean"][int(cmd_in)-1], paths=p, cmd=c)

        elif cfg["tab"] == "TWEAK":
            tweaks = {
                '1': "reg add HKCU\\Software\\Microsoft\\GameBar /v AllowAutoGameMode /t REG_DWORD /d 1 /f",
                '2': "powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
                '3': "reg add HKCU\\System\\GameConfigStore /v GameDVR_Enabled /t REG_DWORD /d 0 /f",
                '4': "taskkill /f /im explorer.exe && start explorer.exe",
                '5': "reg add HKCU\\Software\\Microsoft\\DirectX\\UserGpuPreferences /v Direct3DAppSelection /t REG_DWORD /d 2 /f",
                '6': "netsh int tcp set global autotuninglevel=normal",
                '7': "netsh interface tcp set global ecncapability=enabled",
                '8': "bcdedit /set increaseuserva 3072",
                '9': "powershell -Command \"Set-ProcessMitigation -System -Disable DEP\"",
                '10': "powercfg -h off",
                '11': "reg add HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection /v AllowTelemetry /t REG_DWORD /d 0 /f",
                '12': "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize /v EnableTransparency /t REG_DWORD /d 0 /f",
                '13': "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR /v AppCaptureEnabled /t REG_DWORD /d 0 /f",
                '14': "reg add \"HKCU\\Control Panel\\Mouse\" /v MouseSpeed /t REG_SZ /d 0 /f",
                '15': "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters\" /v EnablePrefetcher /t REG_DWORD /d 0 /f",
                '16': "bcdedit /set disabledynamictick yes",
                '17': "reg add HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management /v FeatureSettingsOverride /t REG_DWORD /d 3 /f",
                '18': "reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 0 /f",
                '19': "reg add \"HKEY_CLASSES_ROOT\\Directory\\Background\\shell\\AnyCode\" /v \"ShowBasedOnVelocityId\" /t REG_DWORD /d 639838 /f",
                '20': "bcdedit /set useplatformclock false && bcdedit /set tscsyncpolicy Enhanced"
            }
            if cmd_in in tweaks:
                smart_action(lang_data[cfg["lang"]]["tweak"][int(cmd_in)-1], cmd=tweaks[cmd_in])

if __name__ == "__main__":
    main()