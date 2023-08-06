import requests,os,sys,json
from colorama import *
from sys import platform
from time import *

init(autoreset=True)


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
    print(
f"""
{Fore.WHITE}
           {Fore.WHITE}
          /^\\
          |-|
          |{Fore.RED}m{Fore.WHITE}|
          |{Fore.RED}c{Fore.WHITE}|
          |{Fore.RED}a{Fore.WHITE}|
          |{Fore.RED}p{Fore.WHITE}|
          |{Fore.RED}i{Fore.WHITE}|
         /|{Fore.RED}!{Fore.WHITE}|\\
        / | | \\
       |  | |  |
       `-\\"\\"\\"-`
     
""")
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
            else:
                data = requests.get(f"http://api.mcapi.run/player/{name}", timeout=5).json()
                print(data[f'{search}'])
    def hypixel_stats(self, name, search=None):
        name = str(name)
        if(name == None):
            print(f"{Fore.RED}please specify a name")
        else:
            if(search == None):
                data = requests.get(f"http://api.mcapi.run/hypixel/{name}", timeout=5).json()
                print(data)
            else:
                data = requests.get(f"http://api.mcapi.run/hypixel/{name}", timeout=5).json()
                print(data[f'{search}'])
        #data = requests.get(f"http://api.mcapi.run/hypixel/{name}", timeout=5).json()
        #print(data)
    def name_droptime(self, name):
        name = str(name)
        if(name == None):
            print(f"{Fore.RED}please specify a name")
        else:
            data = requests.get(f"http://api.mcapi.run/droptime/{name}", timeout=5).json()
            print(data)


def get():
    return options()


def clear_screen():
    if platform == "linux" or platform == "linux2":
        os.system("clear")
    elif platform == "darwin":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")

        