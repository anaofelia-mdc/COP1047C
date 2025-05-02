# COP1047C
Python-MDC_1047
#python library needed
=================
main.py
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
=================
accounts.py
  #This module handles the management of bank accounts: checking, deposit, withdrawals, interest accrual
  import winsound #use this library to make beep sound for the user
  from datetime import datetime
=================
auth.py
  from colorama import Fore,Style #need to install this libary
  import hashlib
  import json
  import os
  from datetime import datetime
================
config.sys
  import os
====================
plotting.py
  import pandas as pd
  import matplotlib.pyplot as plt
  import os
  import numpy as np
========================
reports.py
  import csv
  from datetime import datetime
  import os
=======================
storage.py
  import os
  from datetime import datetime
  import json #library need to load/write json files
  import winsound #use this library to make beep sound for the user
  import hashlib #library needed to create password pash
  from colorama import Fore,Style #need to install this libary 
  import config
========================
transactions.py
  from datetime import datetime
  from storage import save_transaction
============================
utils.py
  import winsound #use this library to make beep sound for the user
  from colorama import Fore,Style #need to install this library
======================

Folder Tree should be
_COP1047c
  .idea
  pythonProject
    .idea
    .venv
    BankingApp
      __pycache__
      data (folder get created on initial load of the program if it does not exists)
      *.py (all programs)
      
    
=============================
CLI  Banking Application Main Features
Below are the main features of the my CLI banking application
1.	User Authentication & Security
o	Login/Logout
o	Password reset

2.	Account Management 
o	Account creation
3.	Transaction Processing
o	Withdraw Money
o	Deposit (Savings)
o	Accrue Interest (only if the last day of the month)
o	View Account Details
o	View Transactions
