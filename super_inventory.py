# _________ SUPERPY'S INVENTORY MODULE _________

# IMPORTS
import os
import pandas as pd

# WORKING DIR & PATHS
wd = os.getcwd()
inv_path = os.path.join(wd, 'inventory.csv')

def main():
    pass

# INVENTORY FUNCTION
def add_inventory(buy_id, buy_product_name, buy_quantity, buy_price_pu, buy_date, expiration_date):
    # Check if inventory.csv already exists in this working directory. 
    # If so, continue and add a new row to the existing csv file.
    if os.path.exists(inv_path):
        # Open existing inventory.csv file into a dataframe with the Pandas Module
        df_inv = pd.read_csv(inv_path)
        # Parsed arguments from the Buy Module of the newly registered purchase are stored in a dictionary.
        new_inv = {
            'Buy_ID': [buy_id],
            'Product_Name': [buy_product_name],
            'Quantity': [buy_quantity],
            'Unit_Price': [buy_price_pu],
            'Total_Price': [round(int(buy_quantity) * float(buy_price_pu),2)],
            'Buy_Date': [buy_date],
            'Expiration_Date': [str(expiration_date)]
        }
        # Dictionary is turned into a second dataframe.
        df_new_inv = pd.DataFrame(new_inv)
        # Merging the existing inventory dataframe with new purchase dataframe
        df_inv = pd.concat([df_inv, df_new_inv], ignore_index=True)

     # If the inventory.csv file does not exist in the current working directory yet, the file will be created following these instructions.
    else:
        # Parsed arguments from the Buy Module of the newly registered purchase are stored in a dictionary.
        new_inv = {
            'Buy_ID': [buy_id],
            'Product_Name': [buy_product_name],
            'Quantity': [buy_quantity],
            'Unit_Price': [buy_price_pu],
            'Total_Price': [round(int(buy_quantity) * float(buy_price_pu),2)],
            'Buy_Date': [buy_date],
            'Expiration_Date': [str(expiration_date)]
        }
        # Dictionary is turned into a dataframe with the Pandas Module.
        df_inv = pd.DataFrame(new_inv)

    # Sort the dataframe by Product_Name, followed by the Expiration_Date
    df_inv.sort_values(by=['Product_Name', 'Expiration_Date'], inplace=True)
    
    # Save the updated dataframe as inventory.csv
    return df_inv.to_csv(inv_path, index=False)

if __name__ == '__main__':
    main()