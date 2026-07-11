from subprocess import run
from requests import get
from os import remove, rmdir, mkdir, walk
from os.path import isdir, isfile, join
import threading
import ctypes

input_txt = r"apps.txt"
temp_exe = r"_temp/temp"
temp_folder = r"_temp"

def main():
    #checking if admin
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Please restart this script as administrator")
        input("Press enter to continue\n> ")
        return

    #opening the links file
    try:
        with open(input_txt, "r", encoding="utf-8") as f:
            links = f.read().split()
    except FileNotFoundError:
        with open(input_txt, "w"): pass
        print("Input file does not exist")
        print("It has been automaticaly created for you")
        input("Press enter to continue\n> ")
        return
    
    #check if we have any links to download
    if not links: print("Links is empty, please add installers to download"); return

    #create the temp folder
    try:
        if not isdir(temp_folder): mkdir(temp_folder)
    except Exception as e: print(f"Error creating _temp folder\nError: {e}"); return

    #download the apps
    threads = []
    for num, link in enumerate(links):
        threads.append(threading.Thread(target=fetch_app, args=(num, link)))
        threads[-1].start()
    
    for thread in threads: thread.join() #wait for all threads to finish downloading

    print("Content installing, please take action")

    #run all of the apps
    for i in range(len(links)):
        try: run(temp_exe + str(i+1))
        except Exception as e:
            print(f"Error ocurred while running file\nError: {e}")

    #clean up the temp folder
    try:
        for full_path, _, files in walk(temp_folder):
            for file in files:
                if isfile(join(full_path, file)):
                    print(f"Deleting {file}")
                    remove(join(full_path, file))
        print("Deleting _temp")
        rmdir(temp_folder)
    except Exception as e:
        print(f"Error deleting temp files, please manualy clean them out.\nError: {e}")
    
    print("Complete.")
    input("Press enter to exit script\n> ")

def fetch_app(num, link):
    print(f"Fetching App {num + 1}...")
    try: request = get(link)
    except Exception as e: print(f"Error downloading .exe\nError: {e}"); return

    print("Content has sucessfuly downloaded")
    exe_name = temp_exe + str(num+1)
    try:
        with open(exe_name + ".exe", "wb") as f:
            f.write(request.content)
    except Exception as e:
        print(f"Error ocurred creating .exe\nLink: {link}\nError: {e}")

main()