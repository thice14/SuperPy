# _________ SUPERPY'S EXPIRY MODULE _________

# IMPORTS
import os
import pandas as pd
import super_time as st
from super_inventory import add_inventory

# WORKING DIR & PATHS
wd = os.getcwd()
inventory_path = os.path.join(wd, 'inventory.csv')
expired_path = os.path.join(wd, 'expired.csv')

# EXPIRY RELATED FUNCTIONS
def main():
    pass

def rem_expired(buy_id):
    # Removes expired products from the inventory.csv file once the expired product is registered in expired.csv
    
    # Open existing inventory.csv file into a dataframe with the Pandas Module
    df = pd.read_csv(inventory_path)
    # Looping through the rows in the dataframe to find the corresponding Buy_ID of the expired product.
    for index, row in df.iterrows():
        if buy_id == row['Buy_ID']:
            # When a match is found, the entire row is dropped from the dataframe
            df.drop(index, inplace=True)
    # Updated dataframe is stored as inventory.csv
    return df.to_csv(inventory_path, index=False)

def reg_expired(buy_id, buy_product_name, buy_quantity, buy_price_pu, buy_date, expiration_date):
    # Registers expired products in the expired.csv file
    # Check if expired.csv already exists in this working directory. 
    # If so, continue and add a new row to the existing csv file.
    if os.path.exists(expired_path):
        # Determine 'today' as per SuperPy's internal calendar with the Super_Time Module
        today = st.today()
        # Open expired.csv in a dataframe
        df_exp = pd.read_csv(expired_path)
        # Parsed arguments of the newly found expired product are stored in a dictionary.
        new_exp = {
            'Buy_ID': [buy_id],
            'Product_Name': [buy_product_name],
            'Quantity': [buy_quantity],
            'Loss_Per_Unit': [0 - buy_price_pu],
            'Total_Loss': [round(0 - int(buy_quantity) * float(buy_price_pu),2)],
            'Buy_Date': [buy_date],
            'Expiration_Date': [expiration_date],
            'Filing Date': [today]
        }
        # Dictionary is turned into a second dataframe.
        df_new_exp = pd.DataFrame(new_exp)
        # Merge the existing expired dataframe with new expired product's dataframe
        df_exp = pd.concat([df_exp, df_new_exp], ignore_index=True)
        # Save the updated dataframe as expired.csv
        df_exp.to_csv(expired_path, index=False)
    
     # If the expired.csv file does not exist in the current working directory yet, 
     # the file will be created as follows.
    else:    
        # Determine 'today' as per SuperPy's internal calendar with the Super_Time Module
        today = st.today()
        # Parsed arguments of the expired product are stored in a dictionary.
        new_exp = {
            'Buy_ID': [buy_id],
            'Product_Name': [buy_product_name],
            'Quantity': [buy_quantity],
            'Loss_Per_Unit': [0 - buy_price_pu],
            'Total_Loss': [round(0 - int(buy_quantity) * float(buy_price_pu),2)],
            'Buy_Date': [buy_date],
            'Expiration_Date': [expiration_date],
            'Filing Date': [today]
        }
        # Dictionary is turned into a dataframe with the Pandas Module.
        df_exp = pd.DataFrame(new_exp)
        # Save the dataframe as expired.csv
        df_exp.to_csv(expired_path, index=False)

    # Pass on the Buy_ID of the expired product in rem_expired function 
    # to remove the expired product from the inventory.csv accordingly
    return rem_expired(buy_id)

def check_expired():
    # Checks the expired.csv file for products that have to be returned to the inventory,
    # after changes in SuperPy's internal calendar

    # Check if expired.csv exists in the working directory
    if os.path.exists(expired_path):
        # If so, open expired.csv in a dataframe with the Pandas Module.
        df_exp = pd.read_csv(expired_path)
        # Determine 'today' as per SuperPy's internal calendar with the Super_Time Module
        today = st.today()
        # Loop through the rows of the dataframe
        for index, row in df_exp.iterrows():
            # Make a datetime object of each expiration date so it can be compared against 'today'
            timestamp = pd.Timestamp(row['Expiration_Date']).date()
            # If 'today' is before or on the expiration date, this product has to be returned 
            # to the inventory and be removed from the expired.csv file
            if today == timestamp or today < timestamp:
                buy_id = row['Buy_ID']
                buy_product_name = row['Product_Name']
                buy_quantity = row['Quantity']
                buy_price_pu = float(0 - row['Loss_Per_Unit'])
                buy_date = pd.Timestamp(row['Buy_Date']).date()
                expiration_date = pd.Timestamp(row['Expiration_Date']).date()
                add_inventory(buy_id, buy_product_name, buy_quantity, buy_price_pu, buy_date, expiration_date)
                df_exp.drop(index, inplace=True)
                df_exp.to_csv(expired_path, index=False)
    # If expired.csv does not exist, there are no expired products to be checked, 
    # hence no further action required. Pass.
    else:
        pass

def check_expiry():
    # Checks the inventory.csv file for expired products
    # Open inventory.csv in a dataframe with the Pandas Module.
    df = pd.read_csv(inventory_path)
    # Determine 'today' as per SuperPy's internal calendar with the Super_Time Module
    today = st.today()
    # Loop through the rows of the dateframe.
    for index, row in df.iterrows():
        # Make a datetime object of each expiration date so it can be compared against 'today'
        timestamp = pd.Timestamp(row['Expiration_Date']).date()
        # If the expiration date has passed, the data is gathered and passed on 
        # to be registered in the expired.csv and eventually be removed from the inventory
        if today > timestamp:
            buy_id = row['Buy_ID']
            product_name = row['Product_Name']
            quantity = row['Quantity']
            price_pu = row['Unit_Price']
            buy_date = pd.Timestamp(row['Buy_Date']).date()
            expiration_date = pd.Timestamp(row['Expiration_Date']).date()
            reg_expired(buy_id, product_name, quantity, price_pu, buy_date, expiration_date)

    # Since check_expiry is always triggered by a change in SuperPy's internal calendar, 
    # the expired.csv will automatically be checked for products which might have to be returned 
    # to the inventory, since the calendar can be turned back in time as well.
    return check_expired()
            
if __name__ == '__main__':
    main()