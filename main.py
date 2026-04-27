import ctypes

if not ctypes.windll.shell32.IsUserAnAdmin():
    print("Please restart this script as administrator")
    input("Press enter to continue\n> ")
    exit(0)

from subprocess import run
from requests import get
from os import remove, rmdir, mkdir

input_txt = r"apps.txt"
temp_exe = r"_temp/temp.exe"
temp_folder = r"_temp"

try:
    with open(input_txt, "r", encoding="utf-8") as f:
        links = f.read().split()
except FileNotFoundError:
    with open(input_txt, "w"): pass
    print("Input file does not exist")
    print("It has been automaticaly created for you")
    input("Press enter to continue\n> ")

try: mkdir(temp_folder)
except: pass

for num, link in enumerate(links):
    print(f"Fetching App {num + 1}...")
    request = get(link)

    if not request.raise_for_status():
        print("Content has sucessfuly downloaded")
        try:
            with open(temp_exe, "wb") as f:
                f.write(request.content)
        except Exception as e:
            print(f"Error ocurred creating .exe\nLink: {link}\nError: {e}")

        print("Content downloaded")
        print("Content installing, please take action")

        try: run(temp_exe)
        except Exception as e:
            print(f"Error ocurred while running file\nError: {e}")

    print("Program has encountered an error while downloading file")

print("Please make sure to complete setup before exiting")
input("Press enter to exit script\n> ")

remove(temp_exe)
rmdir(temp_folder)