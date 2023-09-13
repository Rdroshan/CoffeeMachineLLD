"""
Coffee Machine

Components:
1. coffee machine
2. outlets
3. ingredients
4. beverages

Flow:
customer --> selects a beverage from an outlet n --> checks for ingredients capacity -->
collect those ingredients for the beverage --> prepare beverage --> serve it

When multiple customers are getting beverage, There will be accessing ingredients checks parallely
and collecting those ingredients for the beverage
We'll call this critical section and hence only one customer will be allowed to access it at a time
So ingredients check + collecting ingredients = critical section



Assumptions:
0. I'm initialising the coffee machine with items which are alloted to the input slots coffee machine have.
So if we're adding a beverage which doesn't have the required items in the coffee machine,
IT'LL NOT ALLOW TO ADD THE BEVERAGE CONFIGURATION TO THE MACHINE.
1. Not giving edit option i.e. a added item to the coffee can't be edited
2. An added beverage can't be edited
3. One item to one slot
4. More items can't be allotted once we have initialised coffee machine.
4. All ingredients are liquids and hence unit of capacity is in ml.
"""

from input_slot import InputSlot
from item import Item
from beverage import Beverage
from coffee_machine import CoffeeMachine

if __name__ == "__main__":
    # create coffee machine -
    # Coffee machine with ingredients capacity
    # number of input ingredients slots
    # each ingredients slots have its own capacity with units
    # input_slot1 = InputSlot(capacity=100, unit="ml")
    # CoffeeMachine(

    input_slot1 = InputSlot(name="1", capacity=500, unit="ml")
    input_slot2 = InputSlot(name="2", capacity=500, unit="ml")
    input_slot3 = InputSlot(name="3", capacity=100, unit="ml")
    input_slot4 = InputSlot(name="4", capacity=100, unit="ml")
    input_slot5 = InputSlot(name="5", capacity=100, unit="ml")
    coffee_machine = CoffeeMachine(max_slots=5, output_slots=3, input_slots=[input_slot1, input_slot2, input_slot3, input_slot4, input_slot5])

    ingredient1 = Item(name="hot_water", filled=500, input_slot=input_slot1)
    ingredient2 = Item(name="hot_milk", filled=500, input_slot=input_slot2)
    ingredient3 = Item(name="ginger_syrup", filled=100, input_slot=input_slot3)
    ingredient4 = Item(name="sugar_syrup", filled=100, input_slot=input_slot4)
    ingredient5 = Item(name="tea_leaves_syrup", filled=100, input_slot=input_slot5)

    coffee_machine.add_item(ingredient1)
    coffee_machine.add_item(ingredient2)
    coffee_machine.add_item(ingredient3)
    coffee_machine.add_item(ingredient4)
    coffee_machine.add_item(ingredient5)

    # coffee_machine.add_item(ingredient2) # throws error


    # create beverages, will require ingredients
    ingredients = {"hot_water": 200,"hot_milk": 100, "ginger_syrup": 10, "sugar_syrup": 10, "tea_leaves_syrup": 30}
    beverage1 = Beverage(name="hot_tea", ingredients=ingredients)

    coffee_machine.add_beverage(beverage1)
    # if any ingredient is not supported by coffee machine it'll throw error while defining beverage
    ingredients = {"hot_water": 100, "hot_milk": 100, "chocolate_syrup": 50}
    beverage2 = Beverage(name="hot_chocolate", ingredients=ingredients)

    # should throw error, "Unable to add beverage2 because chocolate_syrup not supported"
    # Because chocolate_syrup is not available
    # the max capacity of an ingredient in coffee machine < beverage's ingredient requirement
    # coffee_machine.add_beverage(beverage2)


    ingredients = { "hot_water": 100, "ginger_syrup": 30, "hot_milk": 400, "sugar_syrup": 50, "tea_leaves_syrup": 30}
    beverage2 = Beverage(name="hot_coffee", ingredients=ingredients)
    coffee_machine.add_beverage(beverage2)


    ingredients = {
        "hot_water": 300,
        "ginger_syrup": 30,
        "sugar_syrup": 50,
        "tea_leaves_syrup": 30
      }
    beverage3 = Beverage(name="black_tea", ingredients=ingredients)
    coffee_machine.add_beverage(beverage3)


    ingredients = {
        "hot_water": 100,
        "ginger_syrup": 30,
        "sugar_syrup": 50,
        "green_mixture": 30
    }
    beverage4 = Beverage(name="green_tea", ingredients=ingredients)
    # coffee_machine.add_beverage(beverage4)


    # Test cases
    # Run these test cases by commenting other outputs

    # flows
    # output1
    # coffee_machine.request_beverage(beverage="hot_tea")
    # coffee_machine.request_beverage(beverage="hot_coffee")
    # coffee_machine.request_beverage(beverage="green_tea")


    # output2
    # coffee_machine.request_beverage(beverage="hot_tea")
    # coffee_machine.request_beverage(beverage="black_tea")
    # coffee_machine.request_beverage(beverage="hot_coffee")



    # output3
    # coffee_machine.request_beverage(beverage="hot_tea")
    # coffee_machine.request_beverage(beverage="black_tea")
    # coffee_machine.request_beverage(beverage="hot_tea")

    # output4
    # # coffee_machine.check_items_current_capacity() # to check capacities
    # coffee_machine.request_beverage(beverage="hot_tea")
    # coffee_machine.request_beverage(beverage="black_tea")
    # # coffee_machine.check_items_current_capacity() to check capacities
    # coffee_machine.refill_item("hot_water", 200)
    # # coffee_machine.check_items_current_capacity() to check capacities
    # coffee_machine.request_beverage(beverage="hot_tea")


    # users can select same item parallely, Use multi-threading to test this
    # Expectation: should throw error for the user when ingredient is running low
    from threading import Thread
    threads = []
    coffee_machine.check_items_current_capacity()
    threads.append(Thread(target=coffee_machine.request_beverage, args=("hot_tea", )))
    threads.append(Thread(target=coffee_machine.request_beverage, args=("hot_tea", )))
    threads.append(Thread(target=coffee_machine.request_beverage, args=("hot_tea", )))
    threads.append(Thread(target=coffee_machine.request_beverage, args=("hot_tea", )))

    for t in threads:
        try:
            t.start()
        except Exception as e:
            print(e)
    for t in threads:
        t.join()

    coffee_machine.check_items_current_capacity()

    # users select different items but have ingredients coincide
    # At this one beverage consumes the ingredient and not available for the other
    # Expectation: should throw error for the user when ingredient is running low


