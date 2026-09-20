from subprocess import Popen
from requests import get
from os import remove, rmdir, mkdir, walk
from os.path import isdir, isfile, join
import threading
import ctypes

INPUT_TXT = r"apps.txt"
TEMP_EXE_NAME = r"_temp/temp"
TEMP_FOLDER = r"_temp"

def read_file():
    #opening the links file
    try:
        with open(INPUT_TXT, "r", encoding="utf-8") as f:
            raw_links = f.read().split()

        #parse the links
        is_link = False
        links = {}
        idx = 0
        for i in raw_links:
            if is_link:
                links[idx] = i
            else:
                idx = i
            is_link = not is_link

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
def fetch_app(num, link):
    #download the .exe
    print(f"Fetching App {num + 1}...")
    try: request = get(link)
    except Exception as e: print(f"Error downloading .exe\nError: {e}"); return

    #save the .exe as a file
    print("Content has sucessfuly downloaded")
    exe_name = TEMP_EXE_NAME + str(num+1)
    try:
        with open(exe_name + ".exe", "wb") as f:
            f.write(request.content)
    except Exception as e:
        print(f"Error ocurred creating .exe\nLink: {link}\nError: {e}")

    #run the correct .exe
    try: Popen(exe_name)
    except Exception as e:
        print(f"Error ocurred while running file\nError: {e}")
def begin_download(links):
    threads = []
    for num, link in enumerate(links):
        threads.append(threading.Thread(target=fetch_app, args=(num, link)))
        threads[-1].start()
    
    for thread in threads: thread.join() #wait for all threads to finish downloading

    print("Content installing, please take action")
def clean_temp():
    try:
        for full_path, _, files in walk(TEMP_FOLDER):
            for file in files:
                if isfile(join(full_path, file)):
                    print(f"Deleting {file}")
                    remove(join(full_path, file))
        print("Deleting _temp")
        rmdir(TEMP_FOLDER)
    except Exception as e:
        print(f"Error deleting temp files, please manualy clean them out.\nError: {e}")

def main():
    #checking if admin
    if not is_admin(): return

    #get the links and order to run
    links = read_file()
    
    #check if we have any links to download
    if not links: print("Links is empty, please add installers to download"); return

    #create the temp folder
    try:
        if not isdir(TEMP_FOLDER): mkdir(TEMP_FOLDER)
    except Exception as e: print(f"Error creating _temp folder\nError: {e}"); return

    #download the apps
    begin_download()

    #clean up the temp folder
    clean_temp()

    #complete installation
    print("Complete.")
    input("Press enter to exit script\n> ")


# main()
print(read_file())