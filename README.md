# SUPERPY

Welcome to the usage guide of SuperPy!

SuperPy is a Command Line Interface to manage the inventory of a supermarket. 

SuperPy is written in Python. 

This usage guide aims to briefly explain the features of this CLI and how to use it. In each section below you will find examples of possible command line input.

All input for the registration of purchases and sales, and the changes in the inventory in time, are stored in CSV files, knowingly:
- bought.csv
- inventory.csv
- sold.csv
- expired.csv

## BUYING

The positional arguments in buying are: Product Name (str), Quantity (int) and Price per Unit (float). The optional arguments are Buy Date and Expiration Date. The default for Buy Date is today, as per SuperPy's internal calendar (more on that later), and the default Expiration Date is 2099-12-31 (i.e. product without an expiry date). All purchases are registered both in the bought.csv and inventory.csv files. These files will automatically be created when the first buy gets registered.

```zsh
python3 super.py buy Banana 10 0.5
python3 super.py buy Banana 10 0.5 --expiration_date 2023-06-18
python3 super.py buy Banana 10 0.5 -ed 2023-06-18
python3 super.py buy Banana 10 0.5 --buy_date 2023-05-01
python3 super.py buy Banana 10 0.5 -bd 2023-05-01 -ed 2023-07-01
```

## SELLING

The positional arguments in buying are: Product Name (str), Quantity (int) and Price per Unit (float). The only optional argument here is Sell Date. The default for Sell Date is today, again, as per SuperPy's internal calendar. All sales are registered in the sold.csv file. File will automatically be created when the first sell gets successfully registered.

```zsh
python3 super.py sell Apple 8 0.6
python3 super.py sell Apple 8 0.6 --sell_date 2023-05-01
python3 super.py sell Apple 8 0.6 -sd 2023-05-01
```

## ADVANCING TIME

SuperPy has its own internal calendar. As long as advanced_time has not been called upon, its current calendar is determined by the Timestamp Module from the Pandas Module. Once advance_time has been used, the current date according to SuperPy is stored in date.txt. This date can be modified over and over by calling on advance_time again. Advance_time has only one postional argument: the number of days (int).  Use a positive integer to advance time, a negative integer to turn back time.

```zsh
python3 super.py advance_time 20
python3 super.py advance_time -10
```

When time is advanced, the inventory.csv file will be checked for possibly unsold products that are now expired. These quantities are removed from the inventory and get registered in the expired.csv file. Or vice versa, when time is turned back, stock that was earlier registered as not sold before the expiration date, becomes now available again in the inventory.

## SET TIME

Through the SET TIME function you can also manually adjust the internal clock to an exact date. It only requires one argument: the desired date in a YYYY-MM-DD format.

```zsh
python3 super.py set_time 2023-05-15
```

## REPORTING

There are three types of reports: Inventory, Revenue and Profit. Report can only be used in combination with one of these three.

```zsh
python3 super.py report inventory
python3 super.py report revenue --moment yesterday
python3 super.py report profit --date 2023
```

### Inventory Report
The inventory report will return a table of all the products available to you as per given date. If no date is given, the report is run with today as the default. Of course, 'today' is again based on SuperPy's internal calendar. There are two optional arguments to chose from: 'date' and 'moment'. 'Date' only accepts the format YYYY-MM-DD as input. For 'moment' you can chose between 'now', 'today', 'tomorrow', and 'yesterday. All self-explanatory, also based on SuperPy's internal calendar.

```zsh
python3 super.py report inventory
python3 super.py report inventory --date 2023-04-18
python3 super.py report inventory -d 2022-03-17
python3 super.py report inventory --moment tomorrow
python3 super.py report inventory -m yesterday
```

### Revenue & Profit Report
Both the revenue and profit report will return a text message with the generated revenue/profit for given day, date or timeframe. As per usual, today is the default argument if none is given. Here, there are the same two optional arguments to chose from: 'date' and 'moment'. There is a slight difference for 'date' compared to the inventory report. Here it also accepts the year (YYYY) or the month of the year (YYYY-MM) as input, as well as the full date (YYYY-MM-DD). For 'moment' you can chose again between 'now', 'today', 'tomorrow', and 'yesterday.

```zsh
python3 super.py report revenue
python3 super.py report revenue --date 2023-04-18
python3 super.py report revenue -d 2023
python3 super.py report revenue -m today
python3 super.py report profit -d 2023-04
python3 super.py report profit -moment yesterday
```
