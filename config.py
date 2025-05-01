import os
import winsound #use this library to make beep sound for the user
# # setup variables here so if someone wants to change them in the future, they can find first
# sub_folder_name = "data"
# # disk file where bank customer logins will be stored

sub_folder_name = "data"
# disk files where data will be stored
bank_user_file = "users.json"
bank_accounts_info_file = "accounts.json"

bank_account_trans_file = "transactions.json"

trans_info_csv_file = "transactions.csv"
trans_info_txt_file = "transactions.txt"

# disk file to store account info such as account number, date opened/close, co-owners, etc.

# transactions can be exported to the file formats indicated below

os.makedirs(sub_folder_name, exist_ok=True)  # if the folder does not exists go ahead and create it

# the variable below will store the file path + file name
bank_user_info = os.path.join(sub_folder_name, bank_user_file)

print(f"loading...bank_user_info : {bank_user_info}")
bank_accounts_info = os.path.join(sub_folder_name, bank_accounts_info_file)
print(f"loading..bank_accounts_info : {bank_accounts_info}")

bank_trans_info = os.path.join(sub_folder_name,bank_account_trans_file)
print(f"loading ..bank_trans_info : {bank_trans_info}")

trans_info_csv= os.path.join(sub_folder_name, trans_info_csv_file)
trans_info_txt = os.path.join(sub_folder_name, trans_info_txt_file)

# create list of file names to be pre-loaded
list_data_files = [bank_user_info, bank_accounts_info, bank_trans_info,trans_info_csv, trans_info_txt]
