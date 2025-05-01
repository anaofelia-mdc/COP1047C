# COP1047C
Python-MDC_1047
#python library needed
import winsound #use this library to make beep sound for the user
from colorama import Fore,Style #need to install this library to see menus in color
import click #need to install this library
from datetime import datetime
import hashlib #library needed to create password pash
import os
import csv
import json #library need to load/write json files
import calendar
import pandas as pd
import matplotlib.pyplot as plt

============================
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
