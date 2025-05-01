#this module generates an on screen report per the user's request
import csv
from datetime import datetime
import os

"""
    parameters in: user_id, trans_data = transaction date, sort_by(date/checking/savings), search_date= YYYY-MM-DD or None
    returns : writes to csv file in the data sub-folder user_id + _ + transactions.csv 
"""
def export_data(user_id, trans_data, file_name, sort_by, search_date):
    if sort_by in ["checking","savings"]:
        trans_data = [i_sort for i_sort in trans_data if i_sort.get("b_acct_type") == sort_by]

    elif sort_by == "date":
        # Filter by trans_date (convert to date part only and compare with search_date)
        search_date = datetime.strptime(search_date, "%Y-%m-%d").date()  # convert user entry of string to date
        trans_data = [
            i_sort for i_sort in trans_data
            if datetime.strptime(i_sort.get("trans_date"), "%Y-%m-%d %H:%M:%S").date() == search_date
        ]

    elif sort_by and sort_by not in ["checking","savings","date"]:
        try:
            trans_data = recursive_sort(trans_data, sort_by) #call sort function recursively

        except KeyError:
            print(f"Invalid sort key {sort_by} ..skipping ")

        except Exception as exp_data_erc:
            print(f"An error occurred..export_data: {exp_data_erc}")


    #make sure output folder exists
    file_dir = os.path.dirname(file_name)
    if file_dir and not os.path.exists(file_dir):
        os.makedirs(file_dir)

    file_name = os.path.join(file_dir, f"{user_id}_{os.path.basename(file_name)}")

    if file_name.endswith('.csv'):
        keys = trans_data[0].keys() if trans_data else []

        input (f' Transactions saved under : {file_name} ..press any key')

        with open(file_name, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(trans_data)
    else:
        with open(file_name, 'w') as f:
            for item in trans_data:
                f.write(str(item) + "\n")

def recursive_sort(data, key): #returns the data sorted as requested by the user
    if len(data) <= 1:
        return data
    pivot = data[0]
    left = [x for x in data[1:] if x[key] <= pivot[key]]
    right = [x for x in data[1:] if x[key] > pivot[key]]
    return recursive_sort(left, key) + [pivot] + recursive_sort(right, key)
