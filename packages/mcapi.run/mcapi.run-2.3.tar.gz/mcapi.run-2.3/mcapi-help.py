import os,colorama
from colorama import *
init(autoreset=True)
print(f"""

{Fore.MAGENTA}import {Fore.LIGHTGREEN_EX}mcapi {Fore.GREEN}# this will import the api package

{Fore.LIGHTGREEN_EX}mcapi{Fore.WHITE}.{Fore.LIGHTYELLOW_EX}init{Fore.WHITE}() {Fore.GREEN}# init the api code ( it will show a rocket if there is no error )

{Fore.LIGHTGREEN_EX}mcapi{Fore.WHITE}.{Fore.LIGHTYELLOW_EX}get{Fore.WHITE}() {Fore.GREEN}# the main get function

{Fore.GREEN}# you can use it as the following:

{Fore.LIGHTGREEN_EX}mcapi{Fore.WHITE}.{Fore.LIGHTYELLOW_EX}get{Fore.WHITE}().{Fore.LIGHTYELLOW_EX}player_info{Fore.WHITE}({Fore.RED}"name"{Fore.WHITE})

{Fore.GREEN}# you can also do:

{Fore.LIGHTGREEN_EX}mcapi{Fore.WHITE}.{Fore.LIGHTYELLOW_EX}get{Fore.WHITE}().{Fore.LIGHTYELLOW_EX}player_info{Fore.WHITE}({Fore.RED}"name"{Fore.WHITE}, {Fore.LIGHTBLUE_EX}search{Fore.WHITE}={Fore.RED}""{Fore.WHITE})

{Fore.GREEN}# you can get hypixel stats and info useing this line:

{Fore.LIGHTGREEN_EX}mcapi{Fore.WHITE}.{Fore.LIGHTYELLOW_EX}get{Fore.WHITE}().{Fore.LIGHTYELLOW_EX}hypixel_stats{Fore.WHITE}({Fore.RED}"name"{Fore.WHITE})

{Fore.GREEN}# and you can get the droptime of a name useing:

{Fore.LIGHTGREEN_EX}mcapi{Fore.WHITE}.{Fore.LIGHTYELLOW_EX}get{Fore.WHITE}().{Fore.LIGHTYELLOW_EX}name_droptime{Fore.WHITE}({Fore.RED}"name"{Fore.WHITE})
""")

def test():
    import mcapi # this will import the api package

    mcapi.init() # init the api code ( it will show a rocket if there is no error )

    mcapi.get() # the main get function

    # you can use it as the following:

    mcapi.get().player_info("name")
    # you can also do:
    mcapi.get().player_info("name", search="")

    # you can get hypixel stats and info useing this line:

    mcapi.get().hypixel_stats("name")

    # and you can get the droptime of a name useing:

    mcapi.get().name_droptime("name")