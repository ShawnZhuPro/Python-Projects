from csv import DictReader, DictWriter
from json import dumps

# Adds an order to a specific date and name
def add_order(date, name, food, price):
  # Creates a dict with user data, such as date, name, etc.
  user_data = {
      "date": date,
      "name": name,
      "food": food,
      "price": price,
  }

  # Opens the CSV in "append text" mode
  with open("Orders.csv", mode="at", newline="") as orders_file:
    fieldnames = ["date", "name", "food", "price"]  # Defines the header to the CSV file
    writer = DictWriter(orders_file, fieldnames=fieldnames)  # Creates a DictWriter object to write data to the CSV file
    writer.writerow(user_data)  # Writes the order information from the "user_data" dictionary for each new row in the CSV file


# Views the order of a specific date and name
def view_orders(date, name):
  orders = []  # Empty list to store order info
  # Opens the CSV in "read" mode
  with open("Orders.csv", mode="rt") as orders_file:
    reader = DictReader(orders_file)  # Creates a DictReader object to read CSV data
    total_price, total_price_with_tax = 0, 0
    SD_tax = 1.0725  # Sales tax for San Diego
    # Loops through each row (order) in the CSV file
    for row in reader:
      # Views the order if the user inputs the correct date and name for the order
      if row['date'] == date:
        if row['name'].lower() == name.lower():
          # Creates a dict with food and price keys and adds it to the "orders" list
          orders.append({
            "food": row['food'], 
            "price": f"${row['price']}",
          })
          total_price += float(row['price'])  # Updates the total price of the order
  total_price_with_tax = round(total_price * SD_tax, 2)  # Final price with tax, rounded to 2 decimal points

  # Prices with $ signs added
  total_price = f"${total_price}"
  total_price_with_tax = f"${total_price_with_tax}"

  # Creates a dict to store order information, including the price of the order
  orders_data = {
    "name": name, 
    "orders": orders, 
    "total_price": total_price,
    "total_price_with_tax": total_price_with_tax,
  }
  # Converts the dict to a "pretty-printed" version of the JSON string and prints it
  order_information = dumps(orders_data, indent=4)
  print(order_information)


# Views all the orders of a specific date
def view_all_orders(date):
  orders_by_name = {}  # Dictionary to store orders grouped by name
  # Opens the CSV in "read" mode
  with open("Orders.csv", mode="rt") as orders_file:
    reader = DictReader(orders_file)  # Creates a DictReader object to read CSV data
    SD_tax = 1.0725  # Sales tax for San Diego
    # Loops through each row (order) in the CSV file
    for row in reader:
      # Views the order if the user inputs the correct date for the order
      if row['date'] == date:
        name = row['name']
        food = row['food']
        price = float(row['price'])
        # Checks if the name exists in the dictionary; if not, a new, empty entry
        if name not in orders_by_name:
          orders_by_name[name] = {
            "orders": [], 
            "total_price": 0, 
            "total_price_with_tax": 0,
          }
        # Adds each order dict to the "orders" list
        orders_by_name[name]["orders"].append({
          "food": food, 
          "price": f"${price}",
        })
        orders_by_name[name]["total_price"] += price

  # Calculates and outputs the total price with tax for each person
  for name, data in orders_by_name.items():
    total_price = data["total_price"]  # Gets the price without tax for each person
    total_price_with_tax = round(total_price * SD_tax, 2)  # Rounds the total price with tax to 2 decimals
    # Updates the prices with a $
    data["total_price"] = f"${total_price}"
    data["total_price_with_tax"] = f"${total_price_with_tax}"

  # Converts the dict to a "pretty-printed" version of the JSON string and prints it
  order_information = dumps(orders_by_name, indent=4)
  print(order_information)


# Removes a certain order according to the user's requirements
def remove_order(date, name, food):
  orders = []
  # Opens the CSV in "read" mode
  with open("Orders.csv", mode="rt") as orders_file:
    reader = DictReader(orders_file) # Creates a DictReader object to read CSV data
    # Adds the information of the orders to the empty "orders" list for every order that isn't to be removed in accordance to the user
    for row in reader:
      if (row['date'] != date or
        row['name'].lower() != name.lower() or
        row['food'].lower() != food.lower()):
          orders.append(row)

  # Writes and replaces the old data with new data (without the order that the user wanted removed)
  with open("Orders.csv", mode="wt", newline="") as orders_file:
    fieldnames = ["date", "name", "food", "price"]  # Defines the header for the CSV
    writer = DictWriter(orders_file, fieldnames=fieldnames)  # Creates a DictWriter object to write data to the CSV file
    writer.writeheader()  # Writes the header since "write text" mode replaces everything in the CSV
    writer.writerows(orders)  # Writes the new order information for each new row in the CSV file

  print(f"{food} removed from your order!")


VIEW, VIEW_ALL, ADD, REMOVE, EXIT = range(1, 6)

options = """
        (1) view orders   
        (2) view all orders   
        (3) add order   
        (4) remove order   
        (5) exit
        
"""

while True:
  choice = int(input(options))

  if choice == VIEW:
    date = input("Enter date (ex: 8/13/23): ")
    name = input("Enter name (ex: Shawn): ")
    view_orders(date, name)
    
  elif choice == VIEW_ALL:
    date = input("Enter date (ex: 8/13/23): ")
    view_all_orders(date)
    
  elif choice == ADD:
    date = input("Enter date (ex: 8/13/23): ")
    name = input("Enter name (ex: Shawn): ")
    food = input("Enter food order: ")
    price = float(input("Enter price: "))
    add_order(date, name, food, price)
    
  elif choice == REMOVE:
    date = input("Enter date (ex: 8/13/23): ")
    name = input("Enter name (ex: Shawn): ")
    food = input("Enter food order: ")
    remove_order(date, name, food)
    
  elif choice == EXIT:
    print("Thanks for using my program!")
    break
