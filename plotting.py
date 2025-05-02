#This module prints a plot of transaction
#import python libraries neeeded

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def output_report(user_id, trans_data):
    # Convert transaction data to a Pandas DataFrame
    df = pd.DataFrame(trans_data)

    # Validate fields
    req_fields = ["user_id", "trans_date", "trans_amount", "trans_type"]
    no_fields = [col for col in req_fields if col not in df.columns]
    if no_fields:
        raise ValueError(f"Missing fields in data: {no_fields}")

    # Filter transactions by user_id
    filter_trans_data = df[df["user_id"] == user_id]

    if filter_trans_data.empty:
        print(f"No transactions were found for {user_id}")
    else:
        print(f"Transactions for user id: {user_id}")
        print(filter_trans_data)

        # Ensure trans_date is in datetime format and extract only the date
        filter_trans_data["trans_date"] = pd.to_datetime(filter_trans_data["trans_date"]).dt.date

        # Assign unique colors to each transaction type
        transaction_types = filter_trans_data["trans_type"].unique()
        color_map = {transaction_type: color for transaction_type, color in zip(transaction_types, plt.cm.tab10.colors)}

        # Plot transactions with unique colors per transaction type
        plt.figure(figsize=(10, 6))
        bars = []
        x_labels = filter_trans_data["trans_date"].unique()  # Get unique dates for x-axis
        x_positions = np.arange(len(x_labels))  # Numeric positions for dates

        bar_width = 0.3 #separate bars

        for i, trans_type in enumerate(transaction_types):
            type_data = filter_trans_data[filter_trans_data["trans_type"] == trans_type]

            # Map trans dates to  x-axis
            x_value = [x_positions[np.where(x_labels == date)[0][0]] for date in type_data["trans_date"]]

            # Offset bars horizontally for each transaction type
            bar = plt.bar(np.array(x_value) + (i * bar_width), type_data["trans_amount"],color=color_map[trans_type], width=bar_width, label=trans_type)
            bars.append(bar)

        # put x-axis labels to dates
        plt.xticks(x_positions + (bar_width * (len(transaction_types) / 2)), x_labels, rotation=45)

        # Add axis labels and title
        plt.xlabel("Transaction Date")
        plt.ylabel("Amount")
        plt.title(f"Transactions for user {user_id}")
        plt.legend(title="Transaction Type")  # Add a legend for the colors
        plt.xticks(rotation=45)  # Rotate x-axis labels for readability
        plt.tight_layout()

        # Save filtered transactions to CSV
        subfolder = "data"
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        save_file = os.path.join(subfolder, f"{user_id}_trans_report.csv")
        try:
            save_plot = os.path.join(subfolder,f"{user_id}_transactions_chart.png")  # File name
            plt.savefig(save_plot, dpi=300, bbox_inches="tight")  # Saves high res
            print(f"Chart saved to {save_plot}")

            filter_trans_data.to_csv(save_file, index=False)
            print(f"Report saved to {save_file}")
        except Exception as e:
            print(f"An error occurred while saving the report: {e}")
        plt.show()  #must be done after saving, otherwise it will clear picture before saving it
    return