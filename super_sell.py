# _________ SUPERPY'S SELL MODULE _________

# IMPORTS
import os
import pandas as pd
from super_expiry import check_expiry
from datetime import datetime
from rich.console import Console
from rich.text import Text

# WORKING DIR & PATHS
wd = os.getcwd()
inv_path = os.path.join(wd, 'inventory.csv')
sold_path = os.path.join(wd, 'sold.csv')

# SELL FUNCTIONS
def main():
    pass

def register_sale(sell_product_name, sell_quantity, sell_price_pu, sell_date, total_profit, buy_id):
    # Registers a sale in the sold.csv file after all checks on availability are complete (function 'selling', see below)

    # Check if bought.csv already exists in this working directory. 
    # If so, continue and add a new row to the existing csv file.
    if os.path.exists(sold_path):
        # Open existing sold.csv file into a dataframe with the Pandas Module
        df_sell = pd.read_csv(sold_path) 
        # First index in the shape method shows the current amount of rows in the bought dataframe. 
        # Using this integer and add 1 to create continiously unique selling IDs.  
        sell_id = 'S'+ str(df_sell.shape[0]+1)
        # Parsed arguments of the new sale are stored in a dictionary.
        sale = {
            'Sell_ID': [sell_id],
            'Product_Name': [sell_product_name],
            'Quantity': [sell_quantity],
            'Unit_Price': [sell_price_pu],
            'Total_Price': [float(round(int(sell_quantity) * float(sell_price_pu),2))],
            'Total_Profit': [total_profit],
            'Sell_Date': [sell_date],
            'Buy_ID': [buy_id]
        }
        # Dictionary is turned into a second dataframe.
        df_new_sell = pd.DataFrame(sale)
        # Merge the existing sold dataframe with new purchase dataframe
        df_sell = pd.concat([df_sell, df_new_sell], ignore_index=True)
        # Save the updated dataframe as sold.csv
        df_sell.to_csv(sold_path, index=False)

    # If the sold.csv file does not exist in the current working directory yet, the file will be created as follows.        
    else:
        # Parsed arguments of the new sale are stored in a dictionary.
        sale = {
            'Sell_ID': ['tbc'],
            'Product_Name': [sell_product_name],
            'Quantity': [sell_quantity],
            'Unit_Price': [sell_price_pu],
            'Total_Price': [float(round(int(sell_quantity) * float(sell_price_pu),2))],
            'Total_Profit': [total_profit],
            'Sell_Date': [sell_date],
            'Buy_ID': [buy_id]
        }
        # Dictionary is turned into a dataframe with the Pandas Module.
        df_sell = pd.DataFrame(sale)
        # First index in the shape method shows the current amount of rows in the sold dataframe. 
        # Using this integer and add 1 to create continiously unique selling IDs.
        # The place holding string is replaced accordingly.
        sell_id = 'S' + str(df_sell.shape[0])
        df_sell.loc[0,'Sell_ID'] = sell_id
        # Save the dataframe as sold.csv
        df_sell.to_csv(sold_path, index=False)

    # Returning a confirmation message in the terminal, styled in Rich, when purchase is successfully registered
    console = Console()
    text = Text("New sale successfully registered in SuperPy's Sell Section!")
    text.stylize('bold cyan on white')

    return console.print(text)


def selling(sell_product_name, sell_quantity, sell_price_pu, sell_date):
    # Function to check the availability of the ordered sale t

    # Check if any inventory exists at all by checking for the existence of the inventory.csv file
    if os.path.exists(inv_path):
        # If file exists, run a check for expired products in the inventory first
        check_expiry()

        # Open existing inventory.csv file into a dataframe with the Pandas Module
        df_inv = pd.read_csv(inv_path)
        # Make a str of the parsed sell_date in order to be comparable in the Pandas DF
        sell_date_str = str(sell_date)
        # Filter Inventory DF for product names and bought before or on the date of selling
        filt = (df_inv['Product_Name'] == sell_product_name) & (df_inv['Buy_Date'] <= sell_date_str)
        # Determine how many available rows are in this dataframe left after filtering
        name_count = df_inv[filt]['Product_Name'].count()
        # Determine the total amount of sellable units in this dataframe after filtering
        name_quantity = df_inv[filt]['Quantity'].sum()

        if name_count == 0:
            print('No such product in stock!')
        else:
            # Check if Quantity of selected Product is sufficient to fullfil Sell Order
            if name_quantity < sell_quantity:
                print('Not enough units in stock!')
            else:
                # Determine the composition of the sale order. 
                # Products from which buy orders are required to fulfill sale order
                quantity_to_deduct = sell_quantity
                total_profit = 0
                buy_id = []
                # Create a while loop that stops once the quantity to deduct = 0
                while quantity_to_deduct > 0:
                    # Loop through the rows of the filtered inventory dataframe
                    for index, row in df_inv[filt].iterrows():
                        # Determine if the quantity found in a row is sufficient to fulfill the remainder of the sale order
                        if row['Quantity'] >= quantity_to_deduct:
                            # If so, register buy_id and total profit
                            buy_id.append(row['Buy_ID'])
                            total_profit += round((quantity_to_deduct * (sell_price_pu - row['Unit_Price'])),2)
                            # Deduct remaining quantity of the sale order from the inventory quantity
                            df_inv.loc[index,'Quantity'] = (row['Quantity'] - quantity_to_deduct)
                            # If after the sale, the remaining quantity in this row is 0, 
                            # the row is removed from the inventory and
                            if df_inv.loc[index,'Quantity'] == 0:
                                df_inv.drop(index, inplace=True)
                            # Updated inventory dataframe is saved as inventory.csv
                            df_inv.to_csv(inv_path, index=False)
                            # Quantity is put to 0 to break out of the while loop
                            quantity_to_deduct = 0
                            # Sale can be registered in a separate file through the register_sale function
                            register_sale(sell_product_name, sell_quantity, sell_price_pu, sell_date, total_profit, buy_id)
                            break
                        # If the quantity of the row is insufficient to complete entire sale order,
                        # the entire quantity is used to partially fulfill sale order.
                        # Buy_ID is appended to corresponding Buy_IDs of which this sale order consists
                        
                        
                        else:
                            buy_id.append(row['Buy_ID'])
                            # Quantity_to_deduct is deducted by the quantity of product found in this row
                            quantity_to_deduct -= row['Quantity']
                            # Total profit is updated by the profit made on the sale of these units
                            total_profit += round((row['Quantity'] * (sell_price_pu - row['Unit_Price'])),2)
                            # Quantity in this row is updated to 0
                            df_inv.loc[index,'Quantity'] = 0
                            # Entire row is removed from the filtered inventory dataframe
                            df_inv.drop(index, inplace=True)
                            # Remaining quantity will be found in the following row(s) until the while is stopped 
                            # when quantity_to_deduct ends up at 0
    else:
        print('No inventory is found. Make sure to buy products first before you sell.') # NOT WORKING YET - FileNotFoundError

if __name__ == '__main__':
    main()
