# _________ SUPERPY'S BUY MODULE _________

# IMPORTS
import os
import pandas as pd
from super_inventory import add_inventory
from rich.console import Console
from rich.text import Text

# WORKING DIR & PATHS
wd = os.getcwd()
bought_path = os.path.join(wd, 'bought.csv')

def main():
    pass

# BUYING FUNCTION
def buying(buy_product_name, buy_quantity, buy_price_pu, buy_date, expiration_date):
    # Check if bought.csv already exists in this working directory. 
    # If so, continue and add a new row to the existing csv file.
    if os.path.exists(bought_path):
        # Open existing csv file into a dataframe with the Pandas Module
        df_buy = pd.read_csv(bought_path)      
        new_buy_id = 'B'+ str(df_buy.shape[0]+1) 
        # First index in the shape method shows the current amount of rows in the bought dataframe. 
        # Using this integer and add 1 to create continiously unique buying IDs

        # Parsed arguments of the new purchase are stored in a dictionary.
        new_purchase = {
            'Buy_ID': [new_buy_id],
            'Product_Name': [buy_product_name],
            'Quantity': [buy_quantity],
            'Unit_Price': [buy_price_pu],
            'Total_Price': [float(round(int(buy_quantity) * float(buy_price_pu),2))],
            'Buy_Date': [buy_date],
            'Expiration_Date': [expiration_date]
        }
        # Dictionary is turned into a second dataframe.
        df_new_pur = pd.DataFrame(new_purchase)
        # Merge the existing bought dataframe with new purchase dataframe
        df_buy = pd.concat([df_buy, df_new_pur], ignore_index=True)
        # Save the updated dataframe as bought.csv
        df_buy.to_csv(bought_path, index=False)

    # If the bought.csv file does not exist in the current working directory yet, the file will be created as follows.
    else:
        # Parsed arguments of the new purchase are stored in a dictionary.
        purchase = {
        'Buy_ID': ['tbc'],
        'Product_Name': [buy_product_name],
        'Quantity': [buy_quantity],
        'Unit_Price': [buy_price_pu],
        'Total_Price': [float(round(int(buy_quantity) * float(buy_price_pu)),2)],
        'Buy_Date': [buy_date],
        'Expiry_Date': [expiration_date]
        }
        # Dictionary is turned into a dataframe with the Pandas Module.
        df_buy = pd.DataFrame(purchase)
        # First index in the shape method shows the current amount of rows in the bought dataframe. 
        # Using this integer and add 1 to create continiously unique buying IDs.
        # The place holding string is replaced accordingly.
        new_buy_id = 'B' + str(df_buy.shape[0])
        df_buy.loc[0,'Buy_ID'] = new_buy_id
        # Save the dataframe as bought.csv
        df_buy.to_csv(bought_path, index=False)
    
    # Newly registered purchase is also added to the inventory.csv file
    add_inventory(new_buy_id, buy_product_name, buy_quantity, buy_price_pu, buy_date, expiration_date) # FUNCTION IMPORTED FROM THE SUPER_INVENTORY MODULE
    
    # Returning a confirmation message in the terminal, styled in Rich, when purchase is successfully registered
    text = Text("New purchase successfully registered in SuperPy's Buy Section!")
    text.stylize('bold cyan on white')

    console = Console()

    return console.print(text)

if __name__ == '__main__':
    main()


