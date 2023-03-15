# Imports
import argparse
import csv
import argparse
from datetime import datetime, date, timedelta
from time import strptime
from tabulate import tabulate


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


def main():


    # Top-level parser
    parser = argparse.ArgumentParser(
        epilog="For subcommand help, enter 'python super.py <subcommand> -h'.")
    subparsers = parser.add_subparsers(
        title="subcommands", prog="python super.py", dest="subcommand")
    
    # Create the parser for the "advance-time" subcommand
    parser_advance_time = subparsers.add_parser(
        "advance_time", description="go to the date n days in the future", help="go to the date n days in the future")
    parser_advance_time.add_argument("days", type=int, help="number of days")
    parser_advance_time.set_defaults(func=advance_time)

    # inventory 
    parser_inventory = subparsers.add_parser(
        "inventory", description="show the current inventory", help="show the current inventory")
    parser_inventory.set_defaults(func=inventory)

    # revenue
    parser_revenue = subparsers.add_parser(
        "revenue", description="show the revenue", help="show the revenue on a date or month")
    parser_revenue.add_argument(
        "-today", action="store_const", const="today", help="show today's revenue")
    parser_revenue.add_argument(
        "-yesterday", action="store_const", const="yesterday", help="show yesterday's revenue")
    parser_revenue.add_argument(
        "-date", type=valid_date, help="show revenue from a specific date")
    parser_revenue.add_argument(
        "-fromdate", type=valid_date, help="show revenue from a specific date onwards")
    parser_revenue.add_argument(
        "-todate", type=valid_date, help="show revenue until a specific date")
    parser_revenue.set_defaults(func=revenue)

    # profit
    parser_profit = subparsers.add_parser(
        "profit", description="show the profit", help="show the profit on a date or month")
    parser_profit.add_argument(
        "-today", action="store_const", const="today", help="show today's profit")
    parser_profit.add_argument(
        "-yesterday", action="store_const", const="yesterday", help="show yesterday's profit")
    parser_profit.add_argument(
        "-date", type=valid_date, help="show profit from a specific date")
    parser_profit.add_argument(
        "-fromdate", type=valid_date, help="show profit from a specific date onwards")
    parser_profit.add_argument(
        "-todate", type=valid_date, help="show profit until a specific date")
    parser_profit.set_defaults(func=profit)

    # buy
    parser_buy = subparsers.add_parser(
        "buy", description="buy a product and store it", help="buy a product and store it")
    parser_buy.add_argument("product", help="product name")
    parser_buy.add_argument("price", type=float,
                            help="buy price")
    parser_buy.add_argument("expiration", type=valid_date,
                            help="expiration date - yyyy-mm-dd")
    parser_buy.add_argument("count", type=int, help="product count")
    parser_buy.set_defaults(func=buy)

    # sell
    parser_sell = subparsers.add_parser(
        "sell", description="sell a product and store it", help="sell a product and store it")
    parser_sell.add_argument("product", help="product name")
    parser_sell.add_argument("price", type=float,
                             help="sales price - float")
    parser_sell.add_argument("count", type=int, help="product count")
    parser_sell.set_defaults(func=sell)

    # Parse the arguments with the function
    args = parser.parse_args()
    if args.subcommand is None:
        parser.print_help()
    else:
        args.func(args)


#FUNCTIONS

# check date format
def valid_date(date_string):

    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        msg = f"{date_string} - please enter a date in the format YYYY-MM-DD".format(
            date_string)
        raise argparse.ArgumentTypeError(msg)


# get next id in file
def get_id(file):
        with open(file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            reader_list = list(reader)
            id = len(reader_list)
            return id

# get products from purchase file
def product_list():
    product_list = []
    with open('bought.csv') as csvfile:
        dictreader = csv.DictReader(csvfile)

        for row in dictreader:
            product = row['product']
            if product not in product_list:
                product_list.append(product)
    product_list.sort()
    return product_list


# get sellable amount
def product_inventory(product, date):
    def amount_sellable():
        # bought and not expired products
        amount_sellable = 0
        with open('bought.csv') as csvfile:
            dictreader = csv.DictReader(csvfile)
            for row in dictreader:
                if row['product'] == product and row['date'] <= date.strftime("%Y-%m-%d") and row['expiration'] > date.strftime("%Y-%m-%d"):
                    amount_sellable += int(row['count'])
            return amount_sellable

    def amount_sold():
        amount_sold = 0
        with open('sold.csv') as csvfile:
            dictreader = csv.DictReader(csvfile)
            for row in dictreader:
                if row['product'] == product and row['date'] <= date.strftime("%Y-%m-%d"):
                    amount_sold += int(row['count'])
            return amount_sold

    amount_sellable = amount_sellable()
    amount_sold = amount_sold()
    product_inventory = amount_sellable - amount_sold
    return product_inventory


# show product inventory
def inventory(args):
    offered_products = product_list()
    today = date.today()

    if len(offered_products) == 0:
        print("there are no products, so no inventory available")
    else:
        table = []
        for product in offered_products:
            inventory = product_inventory(product, today)
            table.append([product, inventory])
            table_headers = ['Product', 'Quantity']
        print(f'{tabulate(table, headers=table_headers, tablefmt="rounded_outline")}')


# write future date in result.txt
def advance_time(args):
    today = date.today()
    days_advanced = args.days
    future_date = today + timedelta(days_advanced)

    filename = "result.txt"

    with open(filename, 'w') as textfile:
        textfile.write(str(future_date))
        print(f'the date in {days_advanced} days is {future_date}')


# get result until entered to_date
def result_to_date(filename, date):
    
    with open(filename) as csvfile:
        dictreader = csv.DictReader(csvfile)
        result = 0
        for row in dictreader:
            if row['date'] <= str(date):
                price_product = row['price']
                count_product = row['count']
                result_product = float(price_product) * float(count_product)
                result += result_product
        return result


# get result from entered from_date onwards
def result_from_date(filename, date):
    
    with open(filename) as csvfile:
        dictreader = csv.DictReader(csvfile)
        result = 0
        for row in dictreader:
            if row['date'] >= str(date):
                price_product = row['price']
                count_product = row['count']
                result_product = float(price_product) * float(count_product)
                result += result_product
        return result
 

# if to_date and from_date both are entered get result from the daterange
def result_daterange(filename, start_date, end_date):
    
    with open(filename) as csvfile:
        dictreader = csv.DictReader(csvfile)
        result = 0
        for row in dictreader:
            if row['date'] >= str(start_date) and row['date'] <= str(end_date):
                price_product = row['price']
                count_product = row['count']
                result_product = float(price_product) * float(count_product)
                result += result_product
        return result
 

# get result based on a date (today, yesterday or specific date)
def result_day(filename, day):

    with open(filename) as csvfile:
        dictreader = csv.DictReader(csvfile)
        result = 0
        for row in dictreader:
            if row['date'] == str(day):
                price_product = row['price']
                count_product = row['count']
                result_product = float(price_product) * float(count_product)
                result += result_product
        return result

# calculate revenue (total of sold products)
def revenue(args):

    if args.today is None and args.yesterday is None and args.date is None and args.todate is None and args.fromdate is None:
        print(
            f"please put in an option - see 'python super.py revenue -h'")
    else:
        if args.today:
            today = date.today()
            revenue = result_day("sold.csv", today)
            print(f"The revenue of today ({today}) is: {revenue}")

        if args.yesterday:
            yesterday = date.today() - timedelta(1)
            revenue = result_day("sold.csv", yesterday)
            print(f"The revenue of yesterday ({yesterday}) is: {revenue}")

        if args.date:
            specific_date = args.date
            revenue = result_day("sold.csv", specific_date)
            print(f"The revenue of {specific_date} is: {revenue}")

        if args.todate and args.fromdate is None:
            to_date = args.todate
            revenue = result_to_date("sold.csv", to_date)
            print(f"The revenue until {to_date} is: {revenue}")

        if args.fromdate and args.todate is None:
            from_date = args.fromdate
            revenue = result_from_date("sold.csv", from_date)
            print(f"The revenue from {from_date} onwards is: {revenue}")

        if args.todate and args.fromdate:
            to_date = args.todate
            from_date = args.fromdate
            revenue = result_daterange("sold.csv", from_date, to_date)

            print(f"The revenue between {from_date} and {to_date} is: {revenue}")

# calculate profit (revenue - costs)
def profit(args):

    if args.today is None and args.yesterday is None and args.date is None and args.todate is None and args.fromdate is None:
        print(
            f"please put in an option - see 'python super.py profit -h'")
    else:
        if args.today:
            today = date.today()
            revenue = result_day("sold.csv", today)
            cost = result_day("bought.csv", today)
            profit = revenue - cost
            print(f"The profit of today ({today}) is: {profit}")

        if args.yesterday:
            yesterday = date.today() - timedelta(1)
            revenue = result_day("sold.csv", yesterday)
            cost = result_day("bought.csv", yesterday)
            profit = revenue - cost
            print(f"The profit of yesterday ({yesterday})is: {profit}")

        if args.date:
            specific_date = args.date
            revenue = result_day("sold.csv", specific_date)
            cost = result_day("bought.csv", specific_date)
            profit = revenue - cost
            print(f"The profit of {specific_date} is: {profit}")

        if args.todate and args.fromdate is None:
            to_date = args.todate
            revenue = result_to_date("sold.csv", to_date)
            cost = result_to_date("bought.csv", to_date)
            profit = revenue - cost
            print(f"The profit until {to_date} is: {profit}")

        if args.fromdate and args.todate is None:
            from_date = args.fromdate
            revenue = result_from_date("sold.csv", from_date)
            cost = result_from_date("bought.csv", from_date)
            profit = revenue - cost
            print(f"The profit from {from_date} onwards is: {profit}")

        if args.todate and args.fromdate:
            to_date = args.todate
            from_date = args.fromdate
            revenue = result_daterange("sold.csv", from_date, to_date)
            cost = result_daterange("bought.csv", from_date, to_date)
            profit = revenue - cost
            print(f"The profit between {from_date} and {to_date} is: {profit}")


# function for purchasing products
def buy(args):

    filename = "bought.csv"
    next_id = get_id(filename)
    today = date.today()
    data = [next_id, args.product, today, args.price,
                args.expiration, args.count]

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

    print(f"purchase recorded")


# function for selling products
def sell(args):
    product = args.product
    selling_date = date.today()
    count = args.count
    # product_stock() excludes expired products
    inventory = product_inventory(product, selling_date)

    # exclude selling more than is in stock on the selling date
    if inventory < count:
        print(f"{product.capitalize()} in stock on {selling_date}: {inventory}.")
        print(
            f"Can't sell {count} with {inventory} in stock.")

    else:
    # append data to csv file
        filename = "sold.csv"
        next_id = get_id(filename)
        today = date.today()
        data = [next_id, args.product, today, args.price, args.count]

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

        print(f"sale recorded")




if __name__ == "__main__":
    main()