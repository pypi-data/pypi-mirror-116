import requests,os,sys,json
from colorama import *
from sys import platform

init(autoreset=True)

def init():
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
        