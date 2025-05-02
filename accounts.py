#This module handles the management of bank accounts: checking, deposit, withdrawals, interest accrual
import winsound #use this library to make beep sound for the user
from datetime import datetime

import config
from BankingApp.storage import update_bank_account
from storage import save_bank_account, load_single_file_data
from colorama import Fore,Style #need to figure out how to install this libary with Github package uploaded : ask professor

from transactions import create_transaction

#main bank account class
class BankAccount:
    def __init__(self, b_user_id, b_acct_type,b_depo_money=0):

        self.b_user_id = b_user_id
        self.b_acct_type = b_acct_type
        self.b_acct_balance = b_depo_money
        self.account_create_date =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # we'll set up this attribute here instead of passing it in

#sub-class for checking account
class CheckingAccount(BankAccount):
    def __init__(self, user_id, b_acct_type, b_depo_money=0):
        super().__init__(user_id, b_acct_type="checking",b_depo_money=b_depo_money)

    #function to process withdrawals
    def withdraw(self, money_request):
        if money_request > 0 and ((self.b_acct_balance - money_request) >= self.b_acct_balance): #not enough funds
            winsound.Beep(500, 500)  # send beep to speaker to get user attention
            input(f"You do not have enough balance{self.b_acct_balance} to withdraw that amount..press any key to continue {money_request}")
        else:
            self.b_acct_balance -= money_request
            #record transaction
            print(f"balance now {self.b_acct_balance}")
            return self.b_acct_balance

#sub class for savings accounts
class SavingAccount(BankAccount):
    def __init__(self, user_id, b_acct_type, b_depo_money=0, rate_int=0.01, interest_bal=0):
        super().__init__(user_id,b_acct_type="savings",b_depo_money=b_depo_money)
        self.rate_int = rate_int
        self.interest_bal = interest_bal
        self.date_interest_earned =   "1901-01-01 00:00:00"

    #function to give customer interest
    def earned_int(self):
        #check if the end of month & add interest
        earned_date = self.date_interest_earned.split(" ")[0]
        today_is =  datetime.now().strftime("%Y-%m-%d")

        if earned_date != today_is:
            earned_interest = self.b_acct_balance * self.rate_int

            self.interest_bal += earned_interest

            self.b_acct_balance += earned_interest
            self.date_interest_earned =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # we'll set up this attribute here instead of passing it in

            print(f"You earned interest for the month of : {earned_interest:.2f} : Interest Balance {self.interest_bal }. Your BALANCE is now: ${self.b_acct_balance}")
            return earned_interest, self.interest_bal, self.b_acct_balance,True

        else:
            earned_interest = 0.0
            print(f"You  ALREADY earned your interest for this month. Here are balances Interest: {self.interest_bal } : Account: {self.b_acct_balance}")

            return earned_interest, self.interest_bal, self.b_acct_balance, False


    # function to process withdrawals
    def withdraw(self, money_request):
        if money_request > 0 and ((self.b_acct_balance - money_request) >= self.b_acct_balance):  # not enough funds
            winsound.Beep(500, 500)  # send beep to speaker to get user attention
            input(f"You do not have enough balance{self.b_acct_balance} to withdraw that amount..press any key to continue {money_request}")
        else:
            self.b_acct_balance -= money_request
            # record transaction
            print(f"balance now {self.b_acct_balance}")
            return self.b_acct_balance

    def get_earned_int_balance(self):
        # interest_bal = self.interest_bal
        print(f"You interest balance is : {self.interest_bal:.2f}. ")
        #return interest_bal, self.b_acct_balance
        return

    #function below allows customer to make a deposit
    def deposit_money(self,deposit_amt):
        self.b_acct_balance += deposit_amt
        return self.b_acct_balance

#function below create bank account object from parent class and sets up json data structure for saving to json file disk
def create_bank_account(user_id, account_type, depo_money, bank_accounts_info):
    #instantiate a new bank account object

    if account_type == "checking":
        new_account = CheckingAccount(user_id,account_type,depo_money)
        #setup variable with the structured data to be written to the json file
        new_bank_account = {
            "user_id":new_account.b_user_id,
            "account_type":new_account.b_acct_type,
            "acc_balance":new_account.b_acct_balance,
            "create_date":new_account.account_create_date
        }
    elif account_type == "savings":
        new_account = SavingAccount(user_id, account_type, depo_money)
        new_bank_account = {
            "user_id":new_account.b_user_id,
            "account_type":new_account.b_acct_type,
            "acc_balance":new_account.b_acct_balance,
            "create_date":new_account.account_create_date,
            "rate_int":new_account.rate_int,
            "interest_bal":new_account.interest_bal,
            "date_interest_earned":new_account.date_interest_earned
        }
    try:
        save_bank_account(new_bank_account,bank_accounts_info) #call the functon which saves the data to the json file
        return True

    except Exception as exc:
        print(f"error {exc}")
        return False

def account_details(user_id):
    assert len(user_id) > 0, "You must log in first.."

#function to display main menu for the account management function
def account_manager(user_id): #this function allows the account owner to perform various tasks on their accounts and it's called from the main menu option
    t_choice=0
    #   f'{Fore.MAGENTA}4 - Account Management{Style.RESET_ALL}\n'
    accounts_menu = (f'{Fore.MAGENTA} CLI BANK - ACCOUNT MANAGEMENT\n'
                     '1 - Create an Account \n'
                     '2 - Withdraw $\n'
                     '3 - Deposit (Savings) $ \n'
                     '4 - Accrue Interest  \n'
                     '5 - View Account Details\n'
                     '6 - View Transactions\n'
                     f'{Fore.RED}7 - Return to previous menu{Style.RESET_ALL}'
                     )
    while t_choice != 7: #EXIT if it is
        try:
            print()
            print(accounts_menu)
            winsound.Beep(500, 500)  # send beep to speaker to get user attention
            t_choice = input("Enter your transaction selection: ").strip().upper()

            if t_choice == "1":
                account_type = input(f'Enter the Account type (C=checking or S=savings):').strip().upper()
                assert account_type == "C" or account_type == "S",f'{Fore.RED}You can ONLY enter C for checking or S for Savings!{Style.RESET_ALL}'

                depo_money = float(input("Enter your initial deposit amount: minimum $25 : "))
                assert depo_money >= 25.0, f'{Fore.RED}You initial deposit must be at least $25 {Style.RESET_ALL}'

                if account_type == "C":
                    account_type = "checking"
                else:
                    account_type = "savings"
                #go ahead call the function w/parameters to create the type of account user requested

                if create_bank_account(user_id, account_type, depo_money, config.bank_accounts_info):
                    #since the account was successfully created go ahead and save it to the json file
                    bln_load, bank_account_data = load_single_file_data(config.bank_accounts_info)

                    if bln_load == True:
                        print(f"Bank Account data re-loaded were preloaded ..press any key")
                        if create_transaction(user_id, account_type, "open", depo_money,config.bank_trans_info):
                            print ("transaction created")
                    else:
                        winsound.Beep(500, 500)  # send beep to speaker to get user attention
                        input(f"{Fore.RED}Bank Account data WAS NOT re-loaded were preloaded ..press any key{Style.RESET_ALL}")
                else:
                    print(f'{Fore.RED}We are UNABLE to create your {account_type} account at this time.. {Style.RESET_ALL}')

            elif t_choice == "2":
                bln_load, bank_account_data = load_single_file_data(config.bank_accounts_info)

                winsound.Beep(500, 500)  # send beep to speaker to get user attention
                a_type = input(f"Choose an account type C = checking , S= savings {user_id}").upper()

                assert a_type in ("C","S"), "Enter only C or S .."
                w_amount = float(input("Enter your amount :"))

                if a_type == 'C':
                    a_type = 'checking'

                elif a_type == 'S':
                    a_type = 'savings'

                for account in bank_account_data["accounts"]:
                    if account['user_id'] == user_id and account['account_type'] == a_type:
                        if a_type == "checking":
                            my_account = CheckingAccount(user_id, a_type, account['acc_balance'])

                        elif a_type == "savings":
                            my_account = SavingAccount(user_id, a_type, account['acc_balance'])

                        new_bal = my_account.withdraw(w_amount)

                        update_bank_account(user_id,a_type,new_bal,0.0,"withdrawal",config.bank_accounts_info)

                        if create_transaction(user_id, a_type, "Withdrawal", w_amount,config.bank_trans_info):
                            print("transaction created...")

            elif t_choice == "3":
                winsound.Beep(500, 500)  # send beep to speaker to get user attention
                bln_load, bank_account_data = load_single_file_data(config.bank_accounts_info)
                a_type = 'savings'
                w_amount = float(input("Enter your deposit amount"))

                for account in bank_account_data["accounts"]:
                    if account['user_id'] == user_id and account['account_type'] == a_type:
                        my_account = SavingAccount(user_id, a_type, account['acc_balance'])

                        new_bal = my_account.deposit_money(w_amount)

                        # input(f"came back from withdrawal {new_bal}")
                        update_bank_account(user_id, a_type, new_bal, 0.0,"deposit",config.bank_accounts_info)
                        if create_transaction(user_id, a_type, "Deposit", w_amount,config.bank_trans_info):
                            print("transaction created...")

            elif t_choice == "4": #accrue interest if it's the last day of the month, otherwise just display what has accrued so far
                today_is = datetime.today()
                what_day_is_it = today_is.day

                month_last_day = calendar.monthrange(today_is.year, today_is.month)[1]
                bln_load, bank_account_data = load_single_file_data(config.bank_accounts_info)
                a_type = 'savings'
                for account in bank_account_data["accounts"]:
                    if account['user_id'] == user_id and account['account_type'] == a_type:
                        if what_day_is_it == month_last_day:

                            my_account = SavingAccount(user_id, a_type, account['acc_balance'])

                            earned_int, interest_bal,new_bal, bln_earned = my_account.earned_int()

                            input(f"earned_int {earned_int} : interest_bal: {interest_bal}")
                            input(f"came back from accrue interest {new_bal} : {earned_int}")

                            if bln_earned:
                                update_bank_account(user_id, a_type, new_bal,interest_bal,"accrual" ,config.bank_accounts_info)

                                if create_transaction(user_id, a_type, "Interest Accrual", earned_int,config.bank_trans_info):
                                 print("transaction created..")
                            else:
                                print(" You ALREADY earned interest for this month ..")
                        else:
                            my_account = SavingAccount(user_id, a_type, account['acc_balance'])
                            interest_bal = my_account.get_earned_int_balance()
                            print(f"Interest Earned so far is: {interest_bal}")

            elif t_choice == "5": #Display account details on the screen
                bln_load, user_bank_data = load_single_file_data(config.bank_accounts_info) # return true/false if file was reloaded
                if not bln_load:
                    winsound.Beep(500, 500)  # send beep to speaker to get user attention
                    input(f'{Fore.RED}Bank User data was NOT reloaded ..press any key {Style.RESET_ALL}')
                    break

                bln_found_trans = False
                try:
                    print()
                    for a_data in user_bank_data['accounts']:
                        if a_data.get('user_id') == user_id:
                            for key, val in a_data.items():
                                if key == "account_type":
                                    print(f"==============Account Details for: {user_id}=======================")
                                    print(f"Account Type: {val.upper()}")
                                if key == "acc_balance":
                                    print (f"Account Balance: {val:.2f}")
                                if key == "interest_bal":
                                    print(f"Interest Earned: {val:.2f}")
                                if key == "rate_int":
                                    print(f"Interest Rate: {val:.2%}")
                                if key == "date_interest_earned":
                                    print(f"Date_Interest_Earned {val}")
                                if key == "create_date":
                                    print(f"Account Created on: {val}")

                            bln_found_trans = True
                            print("======================================")

                        else:
                            bln_found_trans = False

                    print(f'{Fore.YELLOW} Account details displayed... {Style.RESET_ALL}')
                    print()

                except Exception as erc_1:
                    winsound.Beep(500, 500)  # send beep to speaker to get user attention
                    print(f' an error occurred {erc_1}')

                if not bln_found_trans:
                    winsound.Beep(500, 500)  # send beep to speaker to get user attention
                    input(f'{Fore.RED}You have not OPENED any bank accounts yet..press any key to continue {Style.RESET_ALL}')

            elif t_choice == "6":
                # input(f" config.bank_trans_info {config.bank_trans_info}")
                #
                bln_load, trans_bank_data = load_single_file_data(config.bank_trans_info)  # return true/false if file was reloaded
                if not bln_load:
                    winsound.Beep(500, 500)  # send beep to speaker to get user attention
                    input(f'{Fore.RED}Transaction User data was NOT reloaded ..press any key {Style.RESET_ALL}')
                    break

                bln_found_trans = False
                try:
                    print()
                    for a_data in trans_bank_data['transactions']:
                        if a_data.get('user_id') == user_id:
                            for key, val in a_data.items():
                                if key == "b_acct_type":
                                    print(f"==============Transaction History Details for: {user_id}=======================")
                                    print(f"Account Type: {val.upper()}")
                                if key == "trans_type":
                                    print(f"Transaction Type: {val:}")
                                if key == "trans_amount":
                                    print(f"Amount: {val:.2f}")
                                if key == "interest_bal":
                                    print(f"Interest Earned: {val:.2f}")
                                if key == "trans_date":
                                    print(f"Transaction Date: {val}")

                            bln_found_trans = True
                            print("======================================")

                        else:
                            bln_found_trans = False
                    if bln_found_trans:
                        print()
                        print(f'{Fore.YELLOW} Transactions details displayed.. {Style.RESET_ALL}')
                    else:
                        winsound.Beep(500, 500)  # send beep to speaker to get user attention
                        input(f'{Fore.YELLOW} You have NO transactions yet..press any key to continue.. {Style.RESET_ALL}')

                except Exception as erc_1:
                    winsound.Beep(500, 500)  # send beep to speaker to get user attention
                    print(f' an error occurred {erc_1}')

                if not bln_found_trans:
                    winsound.Beep(500, 500)  # send beep to speaker to get user attention
                    input(f'{Fore.YELLOW} You have NO transactions yet..press any key to continue.. {Style.RESET_ALL}')

            elif t_choice == "7":
                break  # go back to calling main menu

        except Exception as erc_1:
            winsound.Beep(500, 500)  # send beep to speaker to get user attention
            print(f' an error occurred {erc_1}')
