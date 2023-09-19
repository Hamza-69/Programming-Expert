import asyncio
from inventory import Inventory
from utils import * 
def display_catalogue(catalogue):
    burgers = catalogue["Burgers"]
    sides = catalogue["Sides"]
    drinks = catalogue["Drinks"]

    print("--------- Burgers -----------\n")
    for burger in burgers:
        item_id = burger["id"]
        name = burger["name"]
        price = burger["price"]
        print(f"{item_id}. {name} ${price}")

    print("\n---------- Sides ------------")
    for side in sides:
        sizes = sides[side]

        print(f"\n{side}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n---------- Drinks ------------")
    for beverage in drinks:
        sizes = drinks[beverage]

        print(f"\n{beverage}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n------------------------------\n")

def welcome():
    print("Welcome to the ProgrammingExpert Burger Bar!")
    print("Loading catalogue...")
    

async def main():
    inventory = Inventory()
    welcome()
    display_catalogue(await inventory.get_catalogue())
    while True:
        await program_loop(inventory)
        x = input("Would you like to make another order (yes/no)? ")
        if x == "no":
            break
    print("Goodbye")

if __name__ == "__main__":
    asyncio.run(main())
