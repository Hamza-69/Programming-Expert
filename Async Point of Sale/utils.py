import asyncio
from copy import deepcopy
from inventory import Inventory

def instructions():
    print("Please enter the number of items that you would like to add to your order. Enter q to complete your order.")

async def choose_item():
    while True:
        x = input("Enter an item number: ")
        if x.isdigit():
            x = int(x)
        elif x == "q":
            return False
        elif not(x.isdigit()):
            print("Please enter a valid number.")
            continue
        if x <= 0:
            print("Please enter a valid number.")
        elif x > 20:
            print("Please enter a number below 21.")
        else:
            return x
async def get_name(item):
    name = ""
    try:
        name = item["name"]
    except KeyError:
        name = item["size"] + " " + item["subcategory"]
    return name

async def order_item(inventory, number):
    return await inventory.get_item(number)

async def order_loop(inventory):
    orders_sch = []
    order_number = 0
    orders = {}
    while True:
        number = await choose_item()
        if not(number):
            break
        orders_sch.append(asyncio.create_task(order_item(inventory, number)))
    for i in orders_sch:
        order_number += 1
        order = await i
        orders[order_number]  = order
    return orders

async def make_orders(inventory, orders):
    order_summary = {}
    faults = []
    if len(orders) == 0:
        return False
    for nb, item in orders.items():
        item_name = await get_name(item)
        if await inventory.decrement_stock(item["id"]):
            order_summary[(item_name,nb) ] = (item["price"], item["category"], item["id"])
            inventory.stock[item["id"]] += 1
        else:
            faults.append(f"Unfortunately item number {item['id']} is out of stock and has been removed from your order. Sorry!")
    return (order_summary, faults)

async def check(inventory, order_summary):
    for i in order_summary.values():
        await inventory.decrement_stock(i[2])

async def crop(item):
    return item[0] if item else False
 
async def combo(orders):
    burgers = deepcopy(orders) 
    burgers = {key: value for key, value in orders.items() if value[1] == "Burgers"}
    burgers = list(burgers.items())
    burgers.sort(key= lambda x: x[1][0])
    sides = deepcopy(orders)
    sides = {key: value for key, value in orders.items() if value[1] == "Sides"}
    sides = list(sides.items())
    sides.sort(key= lambda x: x[1][0])
    drinks = deepcopy(orders)
    drinks = {key: value for key, value in orders.items() if value[1] == "Drinks"}
    drinks = list(drinks.items())
    drinks.sort(key= lambda x: x[1][0])
    combos=[]
    while True:
        burger = await crop(burgers)
        side = await crop(sides)
        drink =  await crop(drinks)
        if burger != False and drink != False and side != False:
            combos.append((burger,side,drink))
            burgers.pop(0)
            sides.pop(0)
            drinks.pop(0)
            del orders[burger[0]]
            del orders[side[0]]
            del orders[drink[0]]
        else:
            break
    if len(combos) == 0:
        return False
    combo_dict = {}
    x = 0
    for i in combos:
        x+=1
        comb = {}
        for j in i:
            comb[j[0]] = j[1]
        combo_dict[x] = comb.copy()
    combos = combo_dict

    return combos

async def program_loop(inventory):
    instructions()
    orders = await order_loop(inventory)
    print("Placing order... \n")
    x = await make_orders(inventory, orders)
    if x == False:
        return
    else:
        order_summary, faults = x
    _summ = deepcopy(order_summary)
    combos = await combo(order_summary)
    print("Here is a summary of your order: \n")
    whole_sum = 0
    if combos != False:
        for i in combos:
            sum = 0
            for j in combos[i].items():
                sum += j[1][0]
            print(f"${round(sum*0.85)} Burger Combo")
            whole_sum += round(sum*0.85)
            for j in combos[i].items():
                print(f"    {j[0][0]}")
    for i in faults:
        print(i)
    print("\n")
    for i in order_summary.items():
        print(f"${i[1][0]} {i[0][0]}")
        whole_sum += i[1][0]
    print("\n")
    print(f"Subtotal: ${round(whole_sum)}")
    print(f"Tax: ${round(whole_sum * 0.05)}")
    print(f"Total: ${round(whole_sum * 1.05)}")
    x = input(f"Would you like to purchase this order for {round(whole_sum * 1.05)} (yes/no)? ")
    if x in ["yes", "y"]:
        await check(inventory, _summ)
        print("Thank you for your order!")
    else:
        print("No problem, please come again!")