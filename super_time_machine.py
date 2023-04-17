# _________ SUPERPY'S TIME MACHINE MODULE _________

# IMPORTS
import os
import datetime as dt
import pandas as pd
from super_expiry import check_expiry
from rich.console import Console
from rich.text import Text

# WORKING DIR & PATHS
wd = os.getcwd()
date_path = os.path.join(wd, 'date.txt')

# FUNCTIONS
def main():
    pass

# Function to advance or turn back time in SuperPy's internal calendar
def time_machine(amount_days):
    # Check if date.txt exists in the working directory
    if os.path.exists(date_path):
        # If file exists, retrieve string from the text file and store it as a datetime obj in a variable
        with open(date_path, "r") as file:
            today_date_str = file.read().strip()
            today_date = dt.datetime.strptime(today_date_str, "%Y-%m-%d")
    # If the file does not exist, current date is determined by Timestamp from Pandas Module.
    else:
        today_date = pd.Timestamp.today().date()

    # Make a datetime object of the given argument in order to move the internal calendar through DT's timedelta
    tdelta = dt.timedelta(amount_days)
    new_date = today_date + tdelta
    # Make a string of the new current date by using strftime
    new_date_str = new_date.strftime("%Y-%m-%d")

    # Store the string of the new date in date.txt in the current working directory for future references
    with open(date_path, "w") as file:
        file.write(new_date_str)
    
    # Once the calendar is changed, inventory has to be checked for potential expired products.
    # Check_expiry will also trigger check_expired. 
    # Check_expired will check expired.csv for products which potentially have to be returned to the inventory
    # due to the change of the internal current date.
    check_expiry()
    
    # Return a text message, styled with the Rich Module, to confirm the new current date.
    text = Text(f'You have travelled to: {new_date_str}')
    text.stylize('bold cyan on white')

    console = Console()

    return console.print(f'You have travelled to: {new_date_str}')

if __name__ == '__main__':
    main()

