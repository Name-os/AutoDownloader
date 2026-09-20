from subprocess import Popen
from requests import get
from os import remove, rmdir, mkdir, walk
from os.path import isdir, isfile, join
import threading
import ctypes

INPUT_TXT = r"apps.txt"
TEMP_EXE_NAME = r"_temp/temp"
TEMP_FOLDER = r"_temp"

def get_links():
    #opening the links file
    try:
        with open(INPUT_TXT, "r", encoding="utf-8") as f:
            raw_links = f.read().split()

        #parse the links
        links = {}
        for _ in range(raw_links):
            link = raw_links.pop()
            idx = raw_links.pop()
            links[idx] = link

        return links
    except FileNotFoundError:
        with open(INPUT_TXT, "w"): pass
        print("Input file does not exist")
        print("It has been automaticaly created for you")
        input("Press enter to continue\n> ")
        return None
def is_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Please restart this script as administrator")
        input("Press enter to continue\n> ")
        return False
    return True

print(get_links())