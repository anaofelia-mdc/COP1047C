#This module contains various function to enable the saving/reading of disk files
import os
from datetime import datetime

import json #library need to load/write json files
# from idlelib.pyparse import trans
# from textwrap import indent

import winsound #use this library to make beep sound for the user
import hashlib #library needed to create password pash
from colorama import Fore,Style #need to install this libary

import config

#function below is called whenever the program loads
def setup_files():
    file_info = {}

    file_info = create_files(
        [config.bank_user_info,
         config.bank_accounts_info,
         config.bank_trans_info,
         config.trans_info_csv,
         config.trans_info_txt])

    print(file_info)

def create_files(file_list):
    print("create_files")
    file_info = {}  # Dictionary to store file contents

    for my_file_name_path in file_list:
        my_file_base_name = os.path.splitext(os.path.basename(my_file_name_path))[0]
        my_extension = os.path.splitext(os.path.basename(my_file_name_path))[1]

        try:
            if not os.path.exists(my_file_name_path) or os.path.getsize(my_file_name_path) == 0:

                # Create the file since it does not exist or is empty
                with open(my_file_name_path, "w",encoding="utf-8") as my_file:

                    if my_extension == ".json":
                        # Create a JSON dictionary with the base name as the key

                        file_dict = {my_file_base_name: []}
                        json.dump(file_dict, my_file, indent=4)
                        # print(f"created {my_file} : {file_dict}")

                    elif my_extension in [".txt", ".csv"]:
                        my_file.write("")

        except json.JSONDecodeError as erc_j:
            print(f' Error decoding JSON file {my_file_name_path}')

        except OSError as erc_os:
            print(f'An OS error occurred: {erc_os}')
            return {}

        except Exception as erc_other:
            print(f'A disk error occurred: {erc_other}')
            return {}

    return file_info  # Return the contents of all files

#search for an existing user
def lookup_user(user_id, user_password, u_choice, user_dict):

    for d_user in user_dict["users"]:
        if d_user.get("user_id") == user_id:
            stored_salt = bytes.fromhex(d_user["salt"])
            stored_hash = d_user["password"]
            stored_create_date = d_user["create_date"]
            new_hash = hashlib.pbkdf2_hmac("sha256", user_password.encode(), stored_salt, 100000).hex()
            if new_hash == stored_hash:  # user entered correct credentials
                if u_choice == 7:
                    winsound.Beep(500, 500)  # send beep to speaker to get user attention
                    print(f"User ID = {user_id} : created on : {stored_create_date} ..press any key")
                return user_id

    return None

def save_user(new_bank_user, bank_user_info):
    print(f' bank_user_info {bank_user_info}')
    # #check if the file/path exists, IF NOT go ahead and create a blank file
    if not os.path.exists(config.bank_user_info) or os.path.getsize(config.bank_user_info) == 0:
        print(f'NOT found it')
        bank_user_data = {"users":[]}
    else:
        print("found it")
        try:
            with open(bank_user_info, "r") as user_file:
                bank_user_data = json.load(user_file)

        except json.JSONDecodeError:
            print(f'{Fore.RED}JSONDecodeError {bank_user_info} not a valid jason file{Style.RESET_ALL}')
            bank_user_data = {"users": []}  # set to an empty dict
            return False

        except FileNotFoundError:
            print(f'{Fore.RED}File NOT found {bank_user_info} {Style.RESET_ALL}')
            return False
        except Exception as ex_erc:
            print(f'{Fore.RED}An error occured {bank_user_info} : {ex_erc} {Style.RESET_ALL}')
            return False

    if bank_user_data is None:
        bank_user_data = {"users": []}  # set to an empty dict
    try:
        bank_user_data["users"].append(new_bank_user) #add the new user
        with open(bank_user_info,"w") as user_file: #add the new user to the physical file
            json.dump(bank_user_data, user_file, indent=4)
        return True

    except Exception as erc_ex:
        print(f'{Fore.RED}An error occurred (in def save_user") {erc_ex}{Style.RESET_ALL}\n')
        return False

def save_bank_account(new_bank_account, bank_account_info):
    # #check if the file/path exists, IF NOT go ahead and create a blank file
    print(f'bank_account_info :{bank_account_info} : {new_bank_account}')
    if not os.path.exists(config.bank_user_info) or os.path.getsize(config.bank_user_info) == 0:
        try:
            with open(bank_account_info, "w") as user_file:
                json.dump({"accounts": []}, user_file, indent=4)

        except json.JSONDecodeError:
            input(f'{Fore.RED}ERROR JSONDecodeError...press any key and Try again{Style.RESET_ALL}')
            return False

    # #open json file for reading
    with open(bank_account_info, "r") as user_file:
        try:
            user_data = json.load(user_file)

        except json.JSONDecodeError:
            user_data = {"accounts": []} #set to an empty dict

        except FileNotFoundError:
            print(f'{Fore.RED}File Not Found Error{Style.RESET_ALL}')
            return False

        except Exception as ex_other:
            print(f'{Fore.RED}An Error occurred {ex_other}{Style.RESET_ALL}')
            return False

    user_data["accounts"].append(new_bank_account)
    with open(bank_account_info,"w") as user_file: #add the new bank to the physical file
        json.dump(user_data, user_file, indent=4)
    return True

def update_bank_account(user_id, a_type,new_bal, int_bal, trans_type,bank_account_info):
    # #check if the file/path exists, IF NOT go ahead and create a blank file
    print(f'update_bank_account : bank_account_info :{bank_account_info} :')
    if not os.path.exists(config.bank_user_info) or os.path.getsize(config.bank_user_info) == 0:
        try:
            with open(bank_account_info, "w") as user_file:
                json.dump({"accounts": []}, user_file, indent=4)

        except json.JSONDecodeError:
            input(f'{Fore.RED}ERROR JSONDecodeError...press any key and Try again{Style.RESET_ALL}')
            return False

    # #open json file for reading
    with open(bank_account_info, "r") as user_file:
        try:
            bank_data = json.load(user_file)

        except json.JSONDecodeError:
            bank_data = {"accounts": []} #set to an empty dict

        except FileNotFoundError:
            print(f'{Fore.RED}File Not Found Error{Style.RESET_ALL}')
            return False

        except Exception as ex_other:
            print(f'{Fore.RED}An Error occurred {ex_other}{Style.RESET_ALL}')
            return False

    bln_found = False

    for my_account in bank_data["accounts"]:
        if my_account["user_id"] == user_id and my_account["account_type"] == a_type:
            bln_found = True
            my_account["acc_balance"] = new_bal

            if my_account["account_type"] == "savings" and trans_type =="accrual":
                my_account["interest_bal"] = int_bal
                my_account["date_interest_earned"]= datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not bln_found:
        print("No account found")
        return False

    # bank_data["accounts"].append(new_bank_account)
    with open(bank_account_info,"w") as user_file: #add the new bank to the physical file
        json.dump(bank_data, user_file, indent=4)
    return True

def save_transaction(new_trans_data, bank_trans_info):
    print(f'bank_trans_info {bank_trans_info} ::{new_trans_data}')
    # #check if the file/path exists, IF NOT go ahead and create a blank file
    if not os.path.exists(config.bank_trans_info) or os.path.getsize(config.bank_trans_info) == 0:
        try:
            with open(bank_trans_info, "w") as trans_file:
                json.dump({"transactions": []}, trans_file, indent=4)

        except json.JSONDecodeError:
            input(f'{Fore.RED}ERROR JSONDecodeError...press any key and Try again{Style.RESET_ALL}')
            return False

    # #open json file for reading
    with open(bank_trans_info, "r") as trans_file:
        try:
            trans_data = json.load(trans_file)

        except json.JSONDecodeError:
            trans_data = {"transactions": []} #set to an empty dict

        except FileNotFoundError:
            print(f'{Fore.RED}File Not Found Error{Style.RESET_ALL}')
            return False

        except Exception as ex_other:
            print(f'{Fore.RED}An Error occurred {ex_other}{Style.RESET_ALL}')
            return False
    print(f"about to append {new_trans_data}")

    trans_data["transactions"].append(new_trans_data) #add the new transaction
    with open(bank_trans_info,"w") as trans_file: #add the new bank to the physical file
        json.dump(trans_data, trans_file, indent=4)

    return True


"""
#pre-load all data files and IF the file does not exists, create an empty file
    load_data_info after a user id is added to the json file
    input params
        list of json/txt files stored in the local drive
        u_choice = menu choice # so we can determined if we called it directly from 
            Register a NEW user or not
    outputs
        returns the contents of all files into the variable file_info - from which we can easily fetch data
            for manipulation
"""
def load_single_file_data(file_name):
    global g_bank_user_data, g_bank_account_data, g_bank_trans_data, g_bank_csv_data, g_bank_txt_data

    my_file_base_name = os.path.splitext(os.path.basename(file_name))[0]
    my_extension = os.path.splitext(os.path.basename(file_name))[1]
    print(f' file_list {file_name} : {my_file_base_name} : {my_extension}')

    try:
        print(f'preloading data {my_file_base_name}..please wait..')
        with open(file_name,"r") as my_file:
            if my_file_base_name == "users" and my_extension == ".json":
                g_bank_user_data = json.load(my_file)
                return True, g_bank_user_data
            elif my_file_base_name == "accounts" and my_extension == ".json":
                g_bank_account_data = json.load(my_file)
                return True, g_bank_account_data
            elif my_file_base_name == "transactions" and my_extension == ".json":
                g_bank_trans_data = json.load(my_file)
                return True, g_bank_trans_data
            elif my_file_base_name == "transactions" and my_extension == ".csv":
                g_bank_csv_data = my_file.read()
                return True, g_bank_csv_data
            elif my_file_base_name == "transactions" and my_extension == ".txt":
                g_bank_txt_data = my_file.read()
                return True, g_bank_txt_data
    # break
    except FileNotFoundError:
        print("FileNotFoundError")
        return False, None
    except Exception as erc_other:
        print(f'A Disk error occurred: {erc_other}')
        return False, None
    except OSError as erc_os:
        print(f'An OS error occurred: {erc_os}')
        return False, None

def load_all_files_data(file_list):
    global g_bank_user_data, g_bank_account_data, _bank_trans_data , g_bank_csv_data, g_bank_txt_data

    for my_file_name_path in file_list:
        my_file_base_name = os.path.splitext(os.path.basename(my_file_name_path))[0]
        my_extension = os.path.splitext(os.path.basename(my_file_name_path))[1]
        try:
            print(f'preloading data {my_file_name_path}..please wait..')

            with open(my_file_name_path,"r") as my_file:
                if my_file_base_name == "users" and my_extension == ".json":
                    g_bank_user_data = json.load(my_file)
                elif my_file_base_name == "accounts" and my_extension == ".json":
                    g_bank_account_data = json.load(my_file)
                elif my_file_base_name == "transactions" and my_extension == ".json":
                    g_bank_trans_data = json.load(my_file)

                elif my_file_base_name == "transactions" and my_extension == ".csv":
                    g_bank_csv_data = my_file.read()
                elif my_file_base_name == "transactions" and my_extension == ".txt":
                    g_bank_txt_data = my_file.read()

        except FileNotFoundError:
            print("FileNotFoundError")
            return False, g_bank_user_data, g_bank_account_data, g_bank_trans_data, g_bank_csv_data, g_bank_txt_data

        except Exception as erc_other:
            print(f'A Disk error occurred: {erc_other}')
            return False, g_bank_user_data, g_bank_account_data, g_bank_trans_data, g_bank_csv_data, g_bank_txt_data

        except OSError as erc_os:
            print(f'An OS error occurred: {erc_os}')
            return False, g_bank_user_data, g_bank_account_data, g_bank_trans_data, g_bank_csv_data, g_bank_txt_data

# # comment lines below after testing/debugging
#     print(type(g_bank_user_data),g_bank_user_data)
#     print(type(g_bank_account_data),g_bank_account_data)
#     print(type(g_bank_trans_data),g_bank_trans_data)
#     print(type(g_bank_csv_data),g_bank_csv_data)
#     print(type(g_bank_txt_data),g_bank_txt_data)
    return True, g_bank_user_data, g_bank_account_data, g_bank_trans_data, g_bank_csv_data, g_bank_txt_data#pre-load was successful

