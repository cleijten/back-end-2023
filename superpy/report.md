### Small functionalities like:
• reporting revenue and profit on a date range, which gives the flexibility to report on whatever daterange you want.
• Generating an id based on the length of the file. Place the rows of the file in a list and get the length of that list. This will be the next id.
• Check lines of bought.csv and sold.csv to calculate the inventory per product. Multiple lines per products will be summarised into one inventory count.

### The use of subparsers:
To be able to use subcommands like ‘buy’, ‘profit’ and ‘inventory’ with different arguments, the use of subparsers is very usefull.

### Tabulate:
I used the tabulate module to nicely print the inventory in a table.
