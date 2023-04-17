# ____________________ SUPERPY'S REPORTING MODULE ____________________

# IMPORTS
import os
import pandas as pd
import calendar as cal
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.text import Text

# WORKING DIR & PATHS
wd = os.getcwd()
bought_path = os.path.join(wd, 'bought.csv')
inv_path = os.path.join(wd, 'inventory.csv')
sold_path = os.path.join(wd, 'sold.csv')
exp_path = os.path.join(wd, 'expired.csv')

# FUNCTIONS
def main():
      pass

# When Buy_ID is found for a sale record, it is appended to a list and saved in the sold DF.
# When the sold DF is stored, the Buy_ID list is turned into a string.
# For example: ['B1'] or ['B1', 'B2']
# Following function will return the Buy_ID string back to a list.
# Basically removes all characters that are NOT 'B' or an integer and then append it to a new list and return it.
def retrieve_buyid(buy_id_string):
    buy_id_string_edit_1 = buy_id_string.replace("'", "")
    buy_id_string_edit_2 = buy_id_string_edit_1.replace(",", "")
    buy_id_string_edit_3 = buy_id_string_edit_2.replace("[", "")
    buy_id_string_edit_4 = buy_id_string_edit_3.replace("]", "")
    id_list = []
    for id in buy_id_string_edit_4.split():
        id_list.append(id)
    return id_list

# Function to determine the total loss in € from expired products
def loss_expired(date_str):
    # Check if expired.csv exists in working directory
    if os.path.exists(exp_path):
        # If so, create a date parser in preparation to read the file as a DF and 
        # turn all Expiration_Dates in a datetime object immediately 
        d_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')
        df_exp = pd.read_csv(exp_path, parse_dates=['Expiration_Date'],date_parser=d_parser)

        # Check if the parsed date has the length of 4 characters, hence potentially being a YYYY string.
        # Thus if the requested report period is a YEAR.
        if len(date_str) == 4:
            # Turn the date string argument in a datetime object for future comparison with the expiration date
            date = datetime.strptime(date_str, "%Y")     
            # Loop through the expired DF       
            for i,r in df_exp.iterrows():
                # If the row is not expired in given year, it is irrelevant, thus dropped from this DF
                if r['Expiration_Date'].year != date.year:
                    df_exp.drop(i, inplace=True)
            # If there are no records found in the remaining DF, the total loss is equal to 0
            if df_exp.empty:
                total_loss = 0
            # Else use the filter + .sum() option to determine the total loss (accumulates all values in the Total_Loss column).
            else:
                total_loss = df_exp['Total_Loss'].sum()

        # Check if the parsed date has the length of 7 characters, hence potentially being a YYYY-MM string.  
        # Thus the requested report is a specific MONTH of a specific YEAR
        elif len(date_str) == 7:
            # Turn the date string argument in a datetime object for future comparison with the expiration date
            date = datetime.strptime(date_str, "%Y-%m")
            # Loop through the rows of the expired DF 
            for i,r in df_exp.iterrows():
                # If the row's Sell_Date's year is equal to the arguments year, continue.
                if r['Sell_Date'].year == date.year:
                    # If the row's Sell_Date's month is also equal to the arguments month, 
                    # this record has to stay in the DF. No further action required (pass)
                    if r['Sell_Date'].month == date.month:
                        pass
                    # If the row's Sell_Date's month is NOT equal to the arguments month, 
                    # the row has to be dropped from this DF since it is irrelevant for this report
                    else:
                        df_exp.drop(i, inplace=True)
                # If the row's Sell_Date's year is NOT equal to the arguments year, 
                # the row has to be dropped from this DF since it is irrelevant for this report
                else:
                    df_exp.drop(i, inplace=True)
            
            # If there are no records found in the remaining DF, the total loss is equal to 0
            if df_exp.empty:
                total_loss = 0
            # Else use the filter + .sum() options available in Pandas to determine the total loss
            # by accumulating the values in the Total_Loss column
            else:
                total_loss = df_exp['Total_Loss'].sum()

        # In case the length is a different amount of characters, it is potentially being a YYYY-MM-DD string.
        else:
            # Turn the date string argument in a datetime object for future comparison with the expiration date
            date = datetime.strptime(date_str, "%Y-%m-%d")
            # In the case of a YYYY-MM-DD datetime object, a specific filter can be applied
            # to immediately show all expired products for that specific expiration date
            filt_exp = (df_exp['Expiration_Date'] == date)
            df_exp_filt = df_exp.loc[filt_exp]

            # If there are no records found in the filtered DF, the total loss is equal to 0
            if df_exp_filt.empty:
                total_loss = 0
            # Else use the .sum() option to determine the total loss by accumulating the values in the Total_Loss column
            else:
                total_loss = df_exp_filt['Total_Loss'].sum()
    
    # If the expired.csv does not exist, total_loss is equal to 0
    else:
        total_loss = 0
    
    return total_loss

# ________________________ INVENTORY REPORT________________________
def inventory_report(inv_date):
    # Give the date from the argument a str format and store it in a new variable (the referral date)
    ref_date = str(inv_date)
    # Open bought.csv in DF
    df_bought = pd.read_csv(bought_path)
    # Filter bought DF for purchases up until referral date and expired products prior given referral date
    filt_b = (df_bought['Buy_Date'] <= ref_date) & (df_bought['Expiration_Date'] > ref_date)
    df_bought_filt = df_bought.loc[filt_b]
    
    # Open sold.csv in DF
    df_sold = pd.read_csv(sold_path)
    # Filter sold DF for sales up until given date
    filt_s = (df_sold['Sell_Date'] <= ref_date)
    df_sold_filt = df_sold.loc[filt_s]
    # Determine if there are sold items to be deducted. 
    # If empty, no sold stock to be deducted per that date.
    if df_sold_filt.empty:
        df_sold = None
    # Else process amounts to be deducted per buy_id
    else:
        # Retrieve buy_ids of the sold products from the DF and change type from str to list
        df_sold_filt['Buy_ID'] = df_sold_filt['Buy_ID'].apply(retrieve_buyid)
        # Iterate over the rows in the filtered sold DF
        for sold_index, sold_row in df_sold_filt.iterrows():
            # Determine total quantity per sale and the according Buy_ID(s)
            sold_quantity = sold_row['Quantity']
            buy_id_sold = sold_row['Buy_ID']
            # Loop over the Buy_ID(s)
            for id in buy_id_sold:
                # Iterate over the rows in the filtered bought DF to match Buy_ID records
                for buy_index, buy_row in df_bought_filt.iterrows():
                    if buy_row['Buy_ID'] == id:
                        # If the total quantity of this Buy_ID was larger than or equal to the sold_quantity, 
                        # it is a simple deduction from the corresponding Buy_ID Quantity in the filtered bought DF
                        if buy_row['Quantity'] >= sold_quantity:
                            df_bought_filt.loc[buy_index, 'Quantity'] = (buy_row['Quantity'] - sold_quantity)
                        # Else, the whole row of this Buy_ID has to be removed from the filt bought DF
                        # And the sold_quantity is deducted by the total remaining quantity of that Buy_ID
                        # The remaining sold_quantity is used in the next loop of the following buy_id
                        else:
                            sold_quantity -= (buy_row['Quantity'])
                            df_bought_filt.drop(buy_index, inplace=True)
    
    # Check if expired.csv exists in working directory
    if os.path.exists(exp_path):
        # If so, open expired.csv in a separate DF
        df_exp = pd.read_csv(exp_path)
        # Filter the DF for products with an expiration date up until referral date
        filt_e = (df_exp['Expiration_Date'] <= ref_date)
        df_exp_filt = df_exp.loc[filt_e]
        # Loop through each row of the filtered EXPIRED DF and temporarily store each row's Buy_ID in a variable
        for exp_index, exp_row in df_exp_filt.iterrows():
            buy_id_exp = exp_row['Buy_ID']
            # Loop through each row of the filtered BOUGHT DF to find a match for the expired Buy_ID
            for buy_index, buy_row in df_bought_filt.iterrows():
                # If Buy_IDs match, the row in the filtered BOUGHT DF is removed entirely
                if buy_row['Buy_ID'] == buy_id_exp:
                    df_bought_filt.drop(buy_index, inplace=True)    
    # If expired.csv file does not exist, the EXPIRED DF remains empty.
    else:
        df_exp = None

    # Rendering a table through the Rich module to present the final DF after all filtering is completed.
    table = Table(
      title='- - - - - - - - - - - -  I N V E N T O R Y  - - - - - - - - - - - -', 
      title_style = 'bold cyan on white', 
      style='cyan')

    show_index = False

    # Loop through the columns of the filtered DF to determine the headers' names and set styling.
    for column in df_bought_filt.columns:
        table.add_column(
            str(column), 
            header_style='bold bright_white on cyan',
            style='bright_white on cyan')
    
    # Loop through each row of the filtered DF to find all values for each column and fill the table
    for index, value_list in enumerate(df_bought_filt.values.tolist()):
            row = [str(index)] if show_index else []
            row += [str(x) for x in value_list]
            table.add_row(*row)

    console = Console()

    return console.print(table)

# ________________________ REVENUE REPORT ________________________

def revenue_report(date_str):
    
    # Check if sold.csv exists in working directory
    if os.path.exists(sold_path):
        # If so, create a date parser in preparation to read the file as a DF and 
        # turn all Expiration_Dates in a datetime object immediately
        d_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')
        df_sold = pd.read_csv(sold_path, parse_dates=['Sell_Date'],date_parser=d_parser)

        # Check if the parsed date has the length of 4 characters, hence potentially being a YYYY string.
        # Thus if the requested report period is a YEAR.
        if len(date_str) == 4:
            # Turn the date string argument in a datetime object for future comparison with the sell date
            date = datetime.strptime(date_str, "%Y")
            # Loop through the rows of the sold DF
            for i,r in df_sold.iterrows():
                # If the row is not sold in given year, it is irrelevant, thus dropped from this DF
                if r['Sell_Date'].year != date.year:
                    df_sold.drop(i, inplace=True)
            # If there are no records found in the remaining DF, report no sales are registered in given year.
            if df_sold.empty:
                text = Text(f'No sales were registered during {date.year}.')
                text.stylize('bold red on white')
            # Else use the filter + .sum() option available in Pandas to determine the total revenue
            # by accumulating all values in the Total_Price column and eventually return the total revenue for the given year
            else:
                total_revenue = df_sold['Total_Price'].sum()
                text = Text(f'In the year {date.year} the total revenue was: €{total_revenue}')
                text.stylize('bold cyan on white')

        # Check if the parsed date has the length of 7 characters, hence potentially being a YYYY-MM string.  
        # Thus the requested report is a specific MONTH of a specific YEAR
        elif len(date_str) == 7:
            # Turn the date string argument in a datetime object for future comparison with the sell date
            date = datetime.strptime(date_str, "%Y-%m")
            # Use the Calendar Module to determine the name of the asked month for future reporting.
            # The integer given by .month is processed by .month_name into the name of that month (1 = January, etc.)
            name_of_month = cal.month_name[date.month]
            # Loop through the rows of the sold DF
            for i,r in df_sold.iterrows():
                # If the row's Sell_Date's year is equal to the arguments year, continue.
                if r['Sell_Date'].year == date.year:
                    # If the row's Sell_Date's month is also equal to the arguments month, 
                    # this record has to stay in the DF. No further action required (pass)                    
                    if r['Sell_Date'].month == date.month:
                        pass
                    # If the row's Sell_Date's month is NOT equal to the arguments month, 
                    # the row has to be dropped from this DF since it is irrelevant for this report                    
                    else:
                        df_sold.drop(i, inplace=True)
                # If the row's Sell_Date's year is NOT equal to the arguments year, 
                # the row has to be dropped from this DF since it is irrelevant for this report                        
                else:
                    df_sold.drop(i, inplace=True)
            
            # If there are no records found in the remaining DF, report no sales are registered in given month.            
            if df_sold.empty:
                text = Text(f'No sales were registered in {name_of_month} {date.year}.')
                text.stylize('bold red on white')
            # Else use the filter + .sum() option available in Pandas to determine the total revenue
            # by accumulating all values in the Total_Price column 
            # and eventually return the total revenue for the given month
            else:
                total_revenue = df_sold['Total_Price'].sum()
                text = Text(f'In {name_of_month} {date.year} the total revenue was: €{total_revenue}')
                text.stylize('bold cyan on white')

        # In case the length is a different amount of characters, it is potentially a YYYY-MM-DD string.
        else:
            # Turn the date string argument in a datetime object for future comparison with the sell date
            date = datetime.strptime(date_str, "%Y-%m-%d")
            # In the case of a YYYY-MM-DD datetime object, a specific filter can be applied
            # to immediately show all sold products on that specific sell date in the sold DF            
            filt = (df_sold['Sell_Date'] == date)
            df_sold_filt = df_sold.loc[filt]
            # If there are no records found in the remaining DF, report no sales are registered on given date.            
            if df_sold_filt.empty:
                text = Text(f'No sales were registered on {date}')
                text.stylize('bold red on white')
            # Else use the .sum() option available in Pandas to determine the total revenue
            # by accumulating all values in the Total_Price column 
            # and eventually return the total revenue for the given date.
            else:
                total_revenue = df_sold_filt['Total_Price'].sum()
                text = Text(f'On {date.date()} the total revenue was: €{total_revenue}')
                text.stylize('bold cyan on white')

    # If there is no sold.csv file found, return no registered sales were found.
    else:
        text = Text(f'No registered sales were found.')
        text.stylize('bold red on white')
    
    # All returned text is styled with the Rich Module
    console = Console()

    return console.print(text)


# ________________________ PROFIT REPORT ________________________

def profit_report(date_str):
    
    # Determine the potential loss from expired products on given date/period (argument).
    # The amount is determined through another function, loss_expired. See above.
    total_loss_expired = loss_expired(date_str)

    # Check if sold.csv exists in working directory
    if os.path.exists(sold_path):
        # If so, create a date parser in preparation to read the file as a DF and 
        # turn all Expiration_Dates in a datetime object immediately
        d_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')
        df_sold = pd.read_csv(sold_path, parse_dates=['Sell_Date'],date_parser=d_parser)

        # Check if the parsed date has the length of 4 characters, hence potentially being a YYYY string.
        # Thus if the requested report period is a YEAR.
        if len(date_str) == 4:
            # Turn the date string argument in a datetime object for future comparison with the sell date
            date = datetime.strptime(date_str, "%Y")
            # Loop through the rows of the sold DF
            for i,r in df_sold.iterrows():
                # If the row is not sold in given year, it is irrelevant, thus dropped from this DF
                if r['Sell_Date'].year != date.year:
                    df_sold.drop(i, inplace=True)
            # If there are no records found in the remaining DF, report no sales are registered in given year.
            if df_sold.empty:
                text = Text(f'No sales were registered during {date.year}.')
                text.stylize('bold red on white')

            # Else use the filter + .sum() option available in Pandas to determine the total profit
            # by accumulating the values in the Total_Profit column. Then deduct the total loss of expired products
            # from the total (gross) profit to eventually return the total (net) profit for given year.
            else:
                total_profit = df_sold['Total_Profit'].sum()
                text = Text(f'In the year {date.year} the total profit was: €{total_profit - total_loss_expired}')
                text.stylize('bold cyan on white')

        # Check if the parsed date has the length of 7 characters, hence potentially being a YYYY-MM string.  
        # Thus the requested report is a specific MONTH of a specific YEAR
        elif len(date_str) == 7:
            # Turn the date string argument in a datetime object for future comparison with the sell date
            date = datetime.strptime(date_str, "%Y-%m")
            # Use the Calendar Module to determine the name of the asked month for future reporting.
            # The integer given by .month is processed by .month_name into the name of that month (1 = January, etc.)
            name_of_month = cal.month_name[date.month]
            # Loop through the rows of the sold DF
            for i,r in df_sold.iterrows():
                # If the row's Sell_Date's year is equal to the arguments year, continue.
                if r['Sell_Date'].year == date.year:
                    # If the row's Sell_Date's month is also equal to the arguments month, 
                    # this record has to stay in the DF. No further action required (pass)
                    if r['Sell_Date'].month == date.month:
                        pass
                    # If the row's Sell_Date's month is NOT equal to the arguments month, 
                    # the row has to be dropped from this DF since it is irrelevant for this report
                    else:
                        df_sold.drop(i, inplace=True)
                # If the row's Sell_Date's year is NOT equal to the arguments year, 
                # the row has to be dropped from this DF since it is irrelevant for this report
                else:
                    df_sold.drop(i, inplace=True)
            
            # If there are no records found in the remaining DF, report no sales are registered in given month.
            if df_sold.empty:
                text = Text(f'No sales were registered in {name_of_month} {date.year}.')
                text.stylize('bold red on white')
            # Else use the filter + .sum() option available in Pandas to determine the total profit
            # by accumulating the values in the Total_Profit column. Then deduct the total loss of expired products
            # from the total (gross) profit to eventually return the total (net) profit for given month.
            else:
                total_profit = df_sold['Total_Profit'].sum()
                text = Text(f'In {name_of_month} {date.year} the total profit was: €{total_profit - total_loss_expired}')
                text.stylize('bold cyan on white')
        
        # In case the length is a different amount of characters, it is potentially a YYYY-MM-DD string.
        else:
            # Turn the date string argument in a datetime object for future comparison with the sell date
            date = datetime.strptime(date_str, "%Y-%m-%d")
            # In the case of a YYYY-MM-DD datetime object, a specific filter can be applied
            # to immediately show all sold products on that specific sell date in the sold DF
            filt = (df_sold['Sell_Date'] == date)
            df_sold_filt = df_sold.loc[filt]
            # If there are no records found in the remaining DF, report no sales are registered on given date.
            if df_sold_filt.empty:
                text = Text(f'No sales were registered on {date}')
                text.stylize('bold red on white')
            # Else use the .sum() option available in Pandas to determine the total profit
            # by accumulating the values in the Total_Profit column. Then deduct the total loss of expired products
            # from the total (gross) profit to eventually return the total (net) profit for given date.
            else:
                total_profit = df_sold_filt['Total_Profit'].sum()
                text = Text(f'On {date.date()} the total profit was: €{total_profit - total_loss_expired}')
                text.stylize('bold cyan on white')
    
    # If there is no sold.csv file found, return no registered sales were found.
    else:
        text = Text(f'No registered sales were found.')
        text.stylize('bold red on white')
    
    # All returned text is styled with the Rich Module
    console = Console()

    return console.print(text)

if __name__ == '__main__':
      main()

