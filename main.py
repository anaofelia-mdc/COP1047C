"""
    Author: Ana-Ofelia Meneses
    Application: CLI Banking Program
"""

#set global variables for later use
g_bank_user_data = None
g_bank_account_data = None
g_bank_trans_data = None
g_bank_csv_data = None
g_bank_txt_data = None

#python library needed
import winsound #use this library to make beep sound for the user
from colorama import Fore,Style #need to install this library to see menus in color
import click #need to install this library

#python modules written by AOM
from BankingApp.reports import export_data
import config #contain variables with names of the files for storing info
from auth import create_user,change_current_password,user_id_duplicate_chk
from plotting import output_report #displays transactions and bar chart for user's transactions
from storage import setup_files, load_single_file_data , load_all_files_data, lookup_user
from utils import disp_msg #displays message either in yellow or red
from accounts import account_manager #handles the account management : create bank account, deposits, withdrawals, etc.

#function below defines the main menu from which user must select a valid #
def show_main_menu():
    click.clear()
    bank_menu_choices = (f'{Fore.BLUE}Welcome to CLI BANK{Style.RESET_ALL}\n'
         f'{Fore.RED}MAIN MENU{Style.RESET_ALL}\n'
         f'{Fore.BLUE}1 - Login {Style.RESET_ALL}\n'
         f'{Fore.YELLOW}2 - Register as a NEW User{Style.RESET_ALL}\n'
         f'{Fore.LIGHTRED_EX}3 - Change Password{Style.RESET_ALL}\n'                      
         f'{Fore.MAGENTA}4 - Account Management{Style.RESET_ALL}\n'
         f'{Fore.GREEN}5 - Export Transaction History{Style.RESET_ALL}\n'
         f'{Fore.WHITE}6 - Reports and Visualizations{Style.RESET_ALL}\n'
         f'{Fore.MAGENTA}7 - LOGOUT{Style.RESET_ALL}\n'
         f'{Fore.RED}8 - EXIT{Style.RESET_ALL}\n'
         )
    winsound.Beep(2000,500) #send beep to speaker to get user attention
    return print(bank_menu_choices,end=' ')

if __name__ == "__main__":
    file_list = setup_files()  #creates files if they do not exist

    # saved_data_file = {} #set

    #pre-load all files where data is stored
    bln_load, g_bank_user_data, g_bank_account_data, g_bank_trans_data, g_bank_csv_data, g_bank_txt_data = load_all_files_data(config.list_data_files)
    if bln_load:
        disp_msg(False,"all files were preloaded..")
    else:
        disp_msg(True, "Some files may not have loaded properly ..press any key..")

    show_main_menu()
    u_choice = 0

    user_id = None # until they logs in or create a new account
    user_password = None

    while u_choice != 8:
        try:
            u_choice = int(input("Enter a valid Menu item #: "))
            match u_choice:

                case 1:  # login existing bank customer
                    user_id = input("Enter your USER ID: ")
                    user_password = input("Enter your password: ")

                    user_id = lookup_user(user_id, user_password, u_choice, g_bank_user_data)

                    if user_id is None:
                        disp_msg(True, "NO User Login found..  Register first ..press any key..")

                        user_id = None
                        current_password = None
                    else:
                        disp_msg(False, f"Welcome back {user_id.upper()} we are glad you are here.. press any..")

                case 2:  # register as NEW bank customer
                    user_id = None
                    user_password = None

                    user_id = input(f"Enter an user id at least 8 characters long:  ")
                    assert len(user_id) >= 8, f"{Fore.RED}Your user ID must be at least 8 characters long {Style.RESET_ALL}"

                    user_password = input("Enter a password at least 8 chars ").strip().lower()
                    assert len(user_password) >= 8, f"{Fore.RED}Your user ID must be at least 8 characters long{Style.RESET_ALL}"
                    assert user_id != user_password,f"{Fore.RED}Your password CANNOT be the same as your user_id{Style.RESET_ALL}"

                    if user_id_duplicate_chk(user_id, config.bank_user_info):
                        disp_msg(True, "User id ALREADY exists. Register first ..press any key..")
                    else:
                        if create_user(user_id, user_password, config.bank_user_info):
                            print(f"ID created/found ..{user_id} press any key")

                            disp_msg(False, "ID created/found ..{user_id} press any key.. ")

                            #re-load the bank  user info into memory
                            bln_load, g_bank_user_data = load_single_file_data(config.bank_user_info)
                            if not bln_load :
                                disp_msg(True, "bank_user_data was not re-loaded.. press any..")
                        else:
                            winsound.Beep(500, 500)  # send beep to speaker to get user attention
                            input(f"{Fore.RED}New User registration FAILED..  try again..press any key{Style.RESET_ALL}")

                case 3: #allow user to change their password
                    winsound.Beep(500, 500)  # send beep to speaker to get user attention

                    user_id = input(f"{Fore.YELLOW}Enter your USER ID: {Style.RESET_ALL}")
                    current_password = input(f"{Fore.YELLOW}Enter your current password: {Style.RESET_ALL}")

                    new_password = input(f"{Fore.RED}Enter your NEW password: {Style.RESET_ALL}")
                    assert new_password != user_password, f"{Fore.RED}Your NEW password CANNOT be the same as your current{Style.RESET_ALL}"
                    assert user_id != new_password, f"{Fore.RED}Your NEW password CANNOT be the same as your USER_ID {Style.RESET_ALL}"

                    if change_current_password(user_id, current_password, new_password,config.bank_user_info):
                        # log-off the user if they were able to change the password and re-load the saved user info
                        user_id = None
                        current_password = None
                        new_password = None

                        bln_load,g_bank_user_data = load_single_file_data(config.bank_user_info)
                        if not bln_load:
                            disp_msg(True, "bank_user_data was not re-loaded.. press any..")
                            user_id = None
                            current_password = None
                            new_password = None

                    else:
                        user_id = None
                        current_password = None
                        new_password = None

                        winsound.Beep(500, 500)  # send beep to speaker to get user attention
                        input(f"{Fore.RED}User ID does NOT exists..  try again..press any key{Style.RESET_ALL}")

                case 4: #account management : bank account

                    if user_id is not None and user_password is not None:
                        account_manager(user_id)
                    else:
                        winsound.Beep(500, 500)  # send beep to speaker to get user attention
                        input(f'{Fore.RED} You must login first..press any key{Style.RESET_ALL}')

                case 5: #export transactions history based on search criteria entered by the user

                    print()

                    if user_id is not None and user_password is not None:
                        search_date = None
                        winsound.Beep(500, 500)  # send beep to speaker to get user attention

                        bln_load, trans_bank_data = load_single_file_data(config.bank_trans_info)
                        trans_data = trans_bank_data['transactions']

                        trans_data = [i_tdata for i_tdata in trans_data if i_tdata.get("user_id") == user_id]
                        if not trans_data:
                            # Check if trans_data contains any records

                            print(f"No Transaction data found for user ID: {user_id} ")
                        else:
                            sort_by = input(f"{Fore.YELLOW}Enter a sort criteria a 1 for date, 2 for checking , 3 for savings OR leave it blank: {Style.RESET_ALL}") or None

                            assert sort_by in ["1","2","3",None], f"{Fore.RED}You can only enter 1 for date, 2 for checking , 3 for savings OR leave it blank for ALL {Style.RESET_ALL}"

                            if sort_by == "1":
                                search_date = input(f"Enter a date YYYY-MM-DD :")
                                sort_by = "date"

                            elif sort_by == "2":
                                sort_by = "checking"

                            elif sort_by == "3":

                                sort_by == "savings"

                            bln_load, trans_bank_data = load_single_file_data(config.bank_trans_info)
                            trans_data = trans_bank_data['transactions']

                            export_data(user_id, trans_data,config.trans_info_csv,sort_by,search_date)
                    else:
                        winsound.Beep(500, 500)  # send beep to speaker to get user attention
                        input(f"{Fore.RED}You must first login ..press any key {Style.RESET_ALL}")

                case 6: #reports

                    if user_id is not None and user_password is not None:
                        bln_load, trans_bank_data = load_single_file_data(config.bank_trans_info)
                        trans_data = trans_bank_data['transactions']

                        trans_data = [i_tdata for i_tdata in trans_data if i_tdata.get("user_id") == user_id]
                        if not trans_data:
                            # Check if trans_data contains any records
                            print(f"No Transaction data found for user ID: {user_id} ")
                        else:
                            output_report(user_id,trans_data)
                    else:
                        winsound.Beep(500, 500)  # send beep to speaker to get user attention
                        input(f"{Fore.RED}You must first login ..press any key {Style.RESET_ALL}")

                case 7: #logout
                    input(f"{Fore.YELLOW}Thank you for your business.press any key {Style.RESET_ALL}")
                    user_id = None
                    user_password = None

                case 8:
                    break

        except Exception as erc_menu:
            print(f"An Error occurred: {erc_menu}")

        # display the main menu and user make a choice
        show_main_menu()

