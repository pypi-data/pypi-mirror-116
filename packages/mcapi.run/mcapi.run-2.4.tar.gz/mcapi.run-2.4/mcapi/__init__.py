import requests,os,sys,json
from colorama import *
from sys import platform
from time import *
import logging

init(autoreset=True)


def cool_text(text):
    for char in str(f"{text}"):
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.05)
    print("\n")

def run():
    if platform == "linux" or platform == "linux2":
        os.system("clear")
    elif platform == "darwin":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    a1 = f"      {Fore.WHITE}/^\\"
    a2 = f" |-|"
    a3 = f"            |{Fore.RED}m{Fore.WHITE}|"
    a4 = f"            |{Fore.RED}c{Fore.WHITE}|"
    a5 = f"            |{Fore.RED}a{Fore.WHITE}|"
    a6 = f"            |{Fore.RED}p{Fore.WHITE}|"
    a7 = f"            |{Fore.RED}p{Fore.WHITE}|"
    a8 = f"           /|{Fore.RED}!{Fore.WHITE}|\\"
    a9 = f"  / | | \\"
    a10 = f"  |  | |  |"
    a11 = f'  `-\\"\\"\\"-`'

    print(' ' * ((os.get_terminal_size().columns - len(a1))//2) + a1)
    print(' ' * ((os.get_terminal_size().columns - len(a2))//2) + a2)
    print(' ' * ((os.get_terminal_size().columns - len(a3))//2) + a3)
    print(' ' * ((os.get_terminal_size().columns - len(a4))//2) + a4)
    print(' ' * ((os.get_terminal_size().columns - len(a5))//2) + a5)
    print(' ' * ((os.get_terminal_size().columns - len(a6))//2) + a6)
    print(' ' * ((os.get_terminal_size().columns - len(a7))//2) + a7)
    print(' ' * ((os.get_terminal_size().columns - len(a8))//2) + a8)
    print(' ' * ((os.get_terminal_size().columns - len(a9))//2) + a9)
    print(' ' * ((os.get_terminal_size().columns - len(a10))//2) + a10)
    print(' ' * ((os.get_terminal_size().columns - len(a11))//2) + a11)
    sleep(1)
    delay23 = 320
    for i in range(50):
        print("")
        sleep(delay23/2000)
        delay23 = delay23 * 0.9






def init(show=None):
    if(show == None or show == True):
        if platform == "linux" or platform == "linux2":
            os.system("clear")
        elif platform == "darwin":
            os.system("clear")
        elif platform == "win32":
            os.system("cls")
        while True:
            try:
                check = requests.get("http://api.mcapi.run/", timeout=1).status_code
                if(check == 200):
                    run()
                    print("tip : open cmd and run 'mcapi-help.py' for a full help script!")
                    sleep(3)
                    break
                else:
                    print(f"{Fore.RED}cant init the api")
                    break
            except requests.Timeout:
                print(f"{Fore.RED}cant init the api")
                break
    if(show == False):
        if platform == "linux" or platform == "linux2":
            os.system("clear")
        elif platform == "darwin":
            os.system("clear")
        elif platform == "win32":
            os.system("cls")
        while True:
            try:
                check = requests.get("http://api.mcapi.run/", timeout=1).status_code
                if(check == 200):
                    break
                else:
                    print(f"{Fore.RED}cant init the api")
                    break
            except requests.Timeout:
                print(f"{Fore.RED}cant init the api")
                break



class options(object):
    def player_info(self, name, search=None):
        name = str(name)
        if(name == None):
            print(f"{Fore.RED}please specify a name")
        else:
            if(search == None):
                data = requests.get(f"http://api.mcapi.run/player/{name}", timeout=5).json()
                print(data)
                logging.info(f"{data}")
            else:
                data = requests.get(f"http://api.mcapi.run/player/{name}", timeout=5).json()
                print(data[f'{search}'])
                logging.info(f"{data}")
    def hypixel_stats(self, name, search=None):
        name = str(name)
        if(name == None):
            print(f"{Fore.RED}please specify a name")
        else:
            if(search == None):
                data = requests.get(f"http://api.mcapi.run/hypixel/{name}", timeout=5).json()
                print(data)
                logging.info(f"{data}")
            else:
                data = requests.get(f"http://api.mcapi.run/hypixel/{name}", timeout=5).json()
                print(data[f'{search}'])
                logging.info(f"{data}")
        #data = requests.get(f"http://api.mcapi.run/hypixel/{name}", timeout=5).json()
        #print(data)
    def name_droptime(self, name):
        name = str(name)
        if(name == None):
            print(f"{Fore.RED}please specify a name")
        else:
            data = requests.get(f"http://api.mcapi.run/droptime/{name}", timeout=5).json()
            print(data)
            logging.info(f"{data}")


def get():
    return options()


def clear_screen():
    if platform == "linux" or platform == "linux2":
        os.system("clear")
    elif platform == "darwin":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")

        