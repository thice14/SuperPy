# _________ SUPERPY'S MAIN MODULE _________

# IMPORTS
import argparse
import super_time as st
from datetime import datetime
from super_buy import buying
from super_sell import selling
from super_report import inventory_report, revenue_report, profit_report
from super_time_machine import time_machine

# WINC REFERENCE ID 
# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.
def main():
    pass

# MAIN SUPERPY PARSER
parser = argparse.ArgumentParser(
    prog='SuperPy',
    description="A command-line tool to register, track, and report your purchases, sales and inventory.",
    epilog="Thank you for using %(prog)s!"
)

# CREATING SUB PARSERS FOR BUY, SELL, REPORT, ADVANCE_TIME
sub_parser = parser.add_subparsers(dest='action', help="Select Buy, Sell, Report or Advance Time")

# BUY PARSER - positional: Product_name, Quantity, Buy_Price_Per_Unit | optional: Buy_Date, Expiration_Date
buy_parser = sub_parser.add_parser('buy', help="Register a purchase")
buy_parser.add_argument('product_name', type=str, help="Enter the name of the product. Singular nouns only please!")
buy_parser.add_argument('quantity', type=int, help="Enter the quantity of the product bought.")
buy_parser.add_argument('buy_price_pu', type=float, help="Enter the purchase price per unit.")
buy_parser.add_argument(
    '-bd', '--buy_date', nargs='?', const=1, default=st.today(), # Today, as per SuperPy's internal calendar, as default.
    type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
    help="Enter the date of the purchase. YYYY-MM-DD (e.g. 2022-12-19). When left out, today, according to SuperPy, is selected by default.")
buy_parser.add_argument(
    '-ed', '--expiration_date', nargs='?', const=1, default='2099-12-31',
    type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
    help="Enter the expiration date of the product. YYYY-MM-DD (e.g. 2023-02-19). Leave blank if there is no expiration date.")

# SELL PARSER - positional: Product_name, Quantity, Sell_Price_Per_Unit | optional: Sell_Date
sell_parser = sub_parser.add_parser('sell', help="Register a sale")
sell_parser.add_argument('product_name', type=str, help="Enter the name of the product. Singular nouns only please!")
sell_parser.add_argument('quantity', type=int, help="Enter the quantity of the product sold.")
sell_parser.add_argument('sell_price_pu', type=float, help="Enter the selling price per unit.")
sell_parser.add_argument(
    '-sd', '--sell_date', nargs='?', const=1, default=st.today(), # Today, as per SuperPy's internal calendar, as default.
    type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
    help="Enter the date of the sale. YYYY-MM-DD (e.g. 2022-12-19). When left out, today, according to SuperPy, is selected by default.")

# REPORT PARSERS
report_parser = sub_parser.add_parser('report', help="Create a report")

# CREATING SUB PARSERS FOR THE 3 REPORT TYPES: INVENTORY / REVENUE / PROFIT
sub_parser_report = report_parser.add_subparsers(dest='report_type', help="Inventory, Revenue or Profit")

# INVENTORY REPORT PARSER - optional + mutually exclusive: Moment (now, today, tomorrow or yesterday) or Date (YYYY-MM-DD)  
inv_report_parser = sub_parser_report.add_parser('inventory', help='Generate an Inventory Report per given moment or date')
inv_report_group = inv_report_parser.add_mutually_exclusive_group()
inv_report_group.add_argument('-m', '--moment', help='Chose a moment in time to generate the report of: now, today, tomorrow or yesterday.',
                               choices=['now', 'today', 'tomorrow', 'yesterday'], nargs='?', const=1, default='today')
inv_report_group.add_argument('-d', '--date', help='Select an exact year, month or date to generate a report of. Format: YYYY-MM-DD.', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date())

# REVENUE REPORT PARSER - optional + mutually exclusive: Moment (now, today, tomorrow or yesterday) or Date (YYYY or YYYY-MM or YYYY-MM-DD)
rev_report_parser = sub_parser_report.add_parser('revenue', help='Generate a Revenue Report')
rev_report_group = rev_report_parser.add_mutually_exclusive_group()
rev_report_group.add_argument('-m', '--moment', help='Chose a moment in time to generate the report of.',
                               choices=['today', 'tomorrow', 'yesterday'], nargs='?', const=1, default='today')
rev_report_group.add_argument('-d', '--date', help='Select an exact year, month or date to generate a report of. Format: YYYY or YYYY-MM or YYYY-MM-DD.', type=str)

# PROFIT REPORT PARSER - optional + mutually exclusive: Moment (now, today, tomorrow or yesterday) or Date (YYYY or YYYY-MM or YYYY-MM-DD)
profit_report_parser = sub_parser_report.add_parser('profit', help='Generate a Profit Report')
profit_report_group = profit_report_parser.add_mutually_exclusive_group()
profit_report_group.add_argument('-m', '--moment', help='Chose a moment in time to generate the report of.',
                               choices=['today', 'tomorrow', 'yesterday'], nargs='?', const=1, default='today')
profit_report_group.add_argument('-d', '--date', help='Select an exact year, month or date to generate a report of. Format: YYYY or YYYY-MM or YYYY-MM-DD.', type=str)

# ADVANCE TIME PARSER -
advance_time_parser = sub_parser.add_parser('advance_time', help="Advance or turn back SuperPy's internal clock by a number of days. Use a positive number to advance time or a negative number to turn back time.")
advance_time_parser.add_argument('number_of_days', type=int, help="Enter the number of days the you would like to advance or turn back internal timing")

# CONCLUDE ALL PARSERS BY CALLING THE PARSE_ARGS
args = parser.parse_args()

# CONVERTING CLI'S ARGUMENTS INTO VARIABLES IN ORDER TO BE PASSED ON FOR FURTHER PROCESSING

# BUYING
if args.action == 'buy':
    buy_product_name = args.product_name
    buy_quantity = args.quantity
    buy_price_pu = args.buy_price_pu
    buy_date = args.buy_date
    expiration_date = args.expiration_date
    buying(buy_product_name, buy_quantity, buy_price_pu, buy_date, expiration_date) # FUNCTION IMPORTED FROM THE SUPER_BUY.PY MODULE

# SELLING
if args.action == 'sell':
    sell_product_name = args.product_name
    sell_quantity = args.quantity
    sell_price_pu = args.sell_price_pu
    sell_date = args.sell_date
    selling(sell_product_name, sell_quantity, sell_price_pu, sell_date) # FUNCTION IMPORTED FROM THE SUPER_SELL.PY MODULE

# REPORTING
if args.action == 'report':
    if args.report_type == 'inventory':
        if args.date:
            date = args.date
        else:
            if args.moment == 'now':
                date = st.now()
            elif args.moment == 'today':
                date = st.today()
            elif args.moment == 'tomorrow':
                date = st.tomorrow()
            elif args.moment == 'yesterday':
                date = st.yesterday()
                
        inventory_report(date) # FUNCTION IMPORTED FROM THE SUPER_REPORT.PY MODULE 

    elif args.report_type == 'revenue':
        if args.date:
            date = args.date
        else:
            if args.moment == 'now':
                date = st.now()
            elif args.moment == 'today':
                date = st.today()
            elif args.moment == 'tomorrow':
                date = st.tomorrow()
            elif args.moment == 'yesterday':
                date = st.yesterday()

        revenue_report(date) # FUNCTION IMPORTED FROM THE SUPER_REPORT.PY MODULE 

    elif args.report_type == 'profit':
        if args.date:
            date = args.date
        else:
            if args.moment == 'now':
                date = st.now()
            elif args.moment == 'today':
                date = st.today()
            elif args.moment == 'tomorrow':
                date = st.tomorrow()
            elif args.moment == 'yesterday':
                date = st.yesterday()

        profit_report(date) # FUNCTION IMPORTED FROM THE SUPER_REPORT.PY MODULE 

# ADVANCING TIME
if args.action == 'advance_time':
    days_to_advance = args.number_of_days
    time_machine(days_to_advance) # METHOD IMPORTED FROM THE SUPER_TIME_MACHINE.PY MODULE 

if __name__ == "__main__":
    main()