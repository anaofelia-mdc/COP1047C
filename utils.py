#declare python libraries needed
import winsound #use this library to make beep sound for the user
from colorama import Fore,Style #need to install this library

#function below will be called when we need to display a message on the screen
#paramaters accepted: True if the message should be displayed in RED and make sure press any key, False if in Yellow
def disp_msg(msg_critical, msg):
    if msg_critical:
        winsound.Beep(500, 500)  # send beep to speaker to get user attention
        input(f'{Fore.RED} {msg} ..press any key to continue{Style.RESET_ALL}')
    else:
        print(f'{Fore.YELLOW} {msg}{Style.RESET_ALL}')