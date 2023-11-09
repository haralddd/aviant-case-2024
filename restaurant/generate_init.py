"""
Generates init.json file for initial database values
Insert all default recurring weekdays (beware, it overwrites new values)
And generates alot of random orders for the database
BEWARE: Uses subprocess to automatically migrate and load,
    probably not safe for production
"""

import json
from datetime import date, timedelta, datetime
import random
import subprocess

def main():
    pk = 0
    recurring_hours = []
    for i in range(0,6):
        recurring_hours.append({
            "model": "staff_interface.RecurringHours",
            "pk": pk,
            "fields": {
                "day": i
                }
            })
        pk += 1
        
    with open('init_hours.json', 'w') as outfile:
        json.dump(recurring_hours, outfile, indent=4)
        
        
    # Generate menu items
    menu_items = []
    menu_item_pks = []
    for i in range(0,10):
        menu_items.append({
            "model": "staff_interface.MenuItem",
            "pk": pk,
            "fields": {
                "name": "Menu Item " + str(i),
                "description": "Description of menu item " + str(i),
                "price": random.randint(10,100)
                }
            }) 
        menu_item_pks.append(pk)
        pk += 1
        
    with open('init_menu_items.json', 'w') as outfile:
        json.dump(menu_items, outfile, indent=4)
    
    # Settings for random orders
    day_span = 30
    start_date = date(2023,11,1)
    example_orders = []
    for i in range(0,100):
        random_date = start_date + timedelta(days=random.randint(0,day_span))
        items = random.choices(menu_item_pks, k=random.randint(1,5))
        example_orders.append({
            "model": "staff_interface.Order",
            "pk": pk,
            "fields": {
                "name": "Example Order " + str(i),
                "phone_number": "12345678",
                "datetime": random_date.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "items": items,
                
                "status": random.randint(0,3),
                }
            })
        pk += 1
        
    with open('init_orders.json', 'w') as outfile:
        json.dump(example_orders, outfile, indent=4)
        
    
    subprocess.run(["python", "manage.py", "makemigrations"])
    subprocess.run(["python", "manage.py", "migrate"])
    subprocess.run(["python", "manage.py", "loaddata", "init_hours.json"])
    subprocess.run(["python", "manage.py", "loaddata", "init_menu_items.json"])
    subprocess.run(["python", "manage.py", "loaddata", "init_orders.json"])
    
            
if __name__ == '__main__':
    main()