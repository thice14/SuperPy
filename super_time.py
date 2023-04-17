# _____________ SUPERPY'S DATETIME MODULE _____________

# IMPORTS
import datetime as dt
import os
import pandas as pd

# WORK DIR & PATHS
wd = os.getcwd()
date_path = os.path.join(wd, 'date.txt')

# FUNCTIONS
def main():
    pass

# Function to determine SuperPy's NOW
def now():
    # Check if date.txt exists in working directory
    if os.path.exists(date_path):
        # If so, open text file and retrieve the date string and turn it into a NOW datetime object
        with open(date_path, "r") as file:
            now_date_str = file.read().strip()
            now_sp = dt.datetime.strptime(now_date_str, '%Y-%m-%d').now()
    # Else, NOW is determined by Timestamp from the Pandas Module.
    else:
        now_sp = pd.Timestamp.now()
    
    return now_sp

# Function to determine SuperPy's TODAY
def today():
    # Check if date.txt exists in working directory
    if os.path.exists(date_path):
        # If so, open text file and retrieve the date string and turn it into a DATE datetime object
        with open(date_path, "r") as file:
            tdy_date_str = file.read().strip()
            tdy_date = dt.datetime.strptime(tdy_date_str, '%Y-%m-%d').date()
    # Else, TODAY is determined by Timestamp from the Pandas Module.
    else:
        tdy_date = pd.Timestamp.today().date()

    return tdy_date

# Function to determine SuperPy's TOMORROW
def tomorrow():
    # Create a datetime timedelta object with value 1, since tomorrow is always current date +1
    tdelta = dt.timedelta(days=1)
    # Determine today datetime object by above function
    tdy_date = today()
    # Tomorrow is today + timedelta(1)
    tmrrw = tdy_date + tdelta

    return tmrrw

# Function to determine SuperPy's YESTERDAY
def yesterday():
    # Create a datetime timedelta object with value 1, since tomorrow is always current date -1
    tdelta = dt.timedelta(days=-1)
    # Determine today datetime object by above function
    tdy_date = today()
    # Tomorrow is today + timedelta(-1)
    ystrdy = tdy_date + tdelta
    
    return ystrdy

if __name__ == '__main__':
    main()