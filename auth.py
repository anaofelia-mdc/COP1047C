#this module contains functions which facilitate the creation of the program users
#saves them to disk

from colorama import Fore,Style #need to install this libary
import hashlib
import json
import os
from datetime import datetime

import storage

#user class to store information for each user - this is different than having a checking/deposit account
class BankUser:
    def __init__(self, user_id, user_password):
        self.user_id = user_id
        self.user_create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.hash_user_password , self.salt = encrypt_password(user_password,salt=None)

#function below will create a hased password via the use of salt
def encrypt_password(user_password, salt=None):
        """
           encode = converts strings into bytes
           sha256 = cryptographic hash function
           pbkdf2_hmac = applies a hash-based msg authentication over 100k iterations as indicated below
           """
        if salt is None:
            salt = os.urandom(16)  # returns a 16 byte random # so we can use in the hash this way the encoded password is always consistently encoded

        hash_user_password = hashlib.pbkdf2_hmac("sha256", user_password.encode(), salt,100000)  # use 100k

        return hash_user_password.hex(), salt.hex()  # convert the hashed password to hexadecimal

#function below allows user to modify their password if they want to
#user must exists
#params in : user_id, current_password, new_password and .json file where users are store in the local folder on disk
def change_current_password(user_id, current_password, new_password, bank_user_info):
    try:
        user_found = False #flag to set True if user found
        with open(bank_user_info,"r") as user_file:
            bank_user_data = json.load(user_file)

            #find the user we are updating the password for
            for find_user in bank_user_data.get("users",[]):
                if user_id == find_user["user_id"]:
                    user_found = True
                    hash_curr_password = find_user["password"]
                    saved_salt = bytes.fromhex(find_user["salt"]) #change salt value back to bytes

                    #use stored salt to rehash current password properlyt
                    old_hash = hashlib.pbkdf2_hmac("sha256", current_password.encode(), saved_salt, 100000).hex()

                    if old_hash == hash_curr_password:
                        if current_password != new_password:
                            hash_user_password_new, salt_new = encrypt_password(new_password)
                            find_user["password"] = hash_user_password_new
                            find_user["salt"] = salt_new
                            break
                        else:
                            input(f'{Fore.RED}Your NEW password CANNOT be the same as your current one...press any key and Try again{Style.RESET_ALL}')
                            return False
                    else:
                        input(f'{Fore.RED}You did NOT enter the correct CURRENT password. No update took place...press any key and Try again{Style.RESET_ALL}')
                        return False
        if user_found:
            with open(bank_user_info,"w") as user_file:
                json.dump(bank_user_data,user_file,indent = 4)
            print(f'{Fore.MAGENTA}Your password was successfully changed ..press any key{Style.RESET_ALL}')
        else:
            return False

    except json.JSONDecodeError:
        input(f'{Fore.RED}ERROR JSONDecodeError...press any key and Try again{Style.RESET_ALL}')
        return False
    except FileNotFoundError:
        input(f'{Fore.RED}The user file storing all users does not appear to exists {bank_user_info}{Style.RESET_ALL}')
        return False
    except Exception as erc_ex:
        input(f'{Fore.RED}an error occurred {erc_ex}in function change_current_password...press any key and Try again{Style.RESET_ALL}')
        return False

    return True

#function below creates login users
def create_user(user_id, user_password, bank_user_info):
    try:
        # check that user does not already exists
        if user_id_duplicate_chk(user_id, bank_user_info):
            input(f'{Fore.RED}User already exists {user_id} ...press any key and Try again{Style.RESET_ALL}')
            return True
        # instantiate a new object of type Bank_User since it does not exists
        b_user = BankUser(user_id, user_password)

        # setup variable with the structured data to be written to the json file
        new_bank_user = {
            "user_id": b_user.user_id,
            "salt": b_user.salt,
            "password": b_user.hash_user_password,
            "create_date": b_user.user_create_date
        }
        storage.save_user(new_bank_user, bank_user_info)
        return True #user created

    except Exception as erc_ex:
        print(f'{Fore.RED}an error occurred in function change_current_password...press any key and Try again{Style.RESET_ALL}')
        return False

#this function verifies bank customer login credentials, if it does not exists THEN ask if they want to create one
#returns the value user_id
def user_id_duplicate_chk(user_id, bank_user_info):
    print(f'bank_user_info {bank_user_info}')
    try:  # check if the bank customer already exists
        if not os.path.exists(bank_user_info) or os.path.getsize(bank_user_info == 0):
            with open(bank_user_info, "w") as user_file:
                try:
                    json.dump({"users": []}, user_file, indent=4)
                    return False
                except Exception as erc:
                    print(f"an error occurred {erc}")
                    return False
        try:
            with open(bank_user_info, "r") as user_file:
                user_json_data = json.load(user_file)
                for find_user in user_json_data.get("users", []):
                    if user_id == find_user["user_id"]:
                        print("An USER id already exists .. enter a different one")
                        return True
            return False
        except json.JSONDecodeError:
            print("Error : JSONDecodeError  json file")
            return False

    except FileNotFoundError:
        input("We are NOT able to log you in at this time. Please contact us at our main branch number!..press any key")
        return False

#function below is called to verify that the user does not already exists
"""
    parameters in: user_id, user_password, bank_user_info (json file users.json)
        u_choice = Since this function can be called from 2 different menu selection
            we need to know how we got here so we execute the right code
            
    this function returns True if the user is found (and this is OK when they logging back
        but should return False when creating a New User
"""
def verify_user(user_id, user_password_, bank_user_info,u_choice):
    try:  #check if the bank customer already exists
        if not os.path.exists(bank_user_info) or os.path.getsize(bank_user_info == 0):
            with open(bank_user_info,"w") as user_file:
                try:
                    json.dump({"users": []}, user_file, indent = 4)
                    return False

                except Exception as erc:
                    print(f"an error occurred {erc}")
                    return False

        with open(bank_user_info, "r") as user_file:
            try:
                user_json_data = json.load(user_file)

            except json.JSONDecodeError:
                print("Error : NO json file")
                user_json_data = {"users": []}
                return False
        if u_choice == 1:
            for find_user in user_json_data.get("users", []):
                if user_id == find_user["user_id"]:
                    print(f'uchoice {u_choice}')
                    stored_salt = bytes.fromhex(find_user["salt"])
                    stored_hash = find_user["password"]
                    new_hash = hashlib.pbkdf2_hmac("sha256", user_password_.encode(), stored_salt, 100000).hex()
                    print(find_user["user_id"], user_id)

                    if new_hash == stored_hash: #user entered correct credentials
                        input(f"{user_id} Welcome back to CLI Bank online banking !..press any key")
                        return True
                    else:
                        print(find_user["user_id"], find_user["password"])
                        input("\nYour password is incorrect. press any key")
                        return False
        if u_choice ==2:
            for find_user in user_json_data.get("users", []):
                if user_id == find_user["user_id"]:
                    print("An USER id already exists .. enter a different one")
                    return True
            return False
    except FileNotFoundError:
        input("We are NOT able to log you in at this time. Please contact us at our main branch number!..press any key")
        return False
