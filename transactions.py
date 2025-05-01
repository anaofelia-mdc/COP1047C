# declare python libraries
from datetime import datetime
from storage import save_transaction

#Transction class will be used to instantiate an obj transaction when users
#conduct such things as open an account, deposit and withdraw money
class Transaction:
    def __init__(self, user_id, b_acct_type,trans_type, trans_amount):
        self.user_id = user_id
        self.b_acct_type = b_acct_type
        self.trans_type = trans_type
        self.trans_amount = trans_amount
        self.trans_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #we'll set up this attribute here instead of passing it in

def create_transaction(user_id, account_type, trans_type, trans_amount,bank_trans_info):
    new_transaction = Transaction(user_id, account_type, trans_type,trans_amount)

    print(f"create_transaction: bank_trans_info {bank_trans_info}")

    new_trans_data = {
        "user_id":new_transaction.user_id,
        "b_acct_type":new_transaction.b_acct_type,
        "trans_type":new_transaction.trans_type,
        "trans_amount":new_transaction.trans_amount,
        "trans_date":new_transaction.trans_date
    }
    try:
        print(f"calling save_transaction {bank_trans_info} {new_trans_data}")
        save_transaction(new_trans_data,bank_trans_info) #call the functon which saves the data to the json file
        return True

    except Exception as exc:
        print(f"error {exc}")
        return False
