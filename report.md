# SuperPy - REPORT


### -- *3 Highlighted Features of SuperPy's code* --

In this report I will highlight 3 features from the coding of SuperPy which I consider noteworthy.


#### **1. Sub-Parsers**

The use of subparsers has led to two advantages. First of all, the input requires very little optional arguments. Hence, less typing and less error prone. Secondly, it automatically limits the input accepted by the CLI, without additional coding through 'choices' and 'mutually exclusive groups'. Furthermore can these limits be clearly returned to the user through the help section or, in case of a wrong entry, a message.


#### **2. Check_Expiry / Expired**

At key moments, like selling or creating an inventory report, the inventory has to be checked for the availability of non-expired products. To do so, the products of the inventory are checked for their expiration date against, what SuperPy considers to be, today. Expired products are first registered in the expired.csv file and subsequently removed from the inventory. 

Whenever inventory is checked for expired products, expired.csv is checked for products that might no longer be considered to be expired. This can happen when the internal calendar of SuperPy has been changed. If that is the case, the products will automatically be returned to the inventory and removed from the expired products database.


#### **3. Creating Buy_ID / Sell_ID**

Since in no way through the script itself, rows are removed from the bought.csv or sold.csv file, the number of rows can be used as indicator. In the Pandas Module exists the 'shape' method. Through indexing the current number of rows can easily be subtracted. This number +1 is then used to create a unique ID for the new purchase or sale.