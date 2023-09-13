
from typing import List
from input_slot import InputSlot
from item import Item
from beverage import Beverage
from threading import Lock

lock = Lock()


class CoffeeMachine:
    def __init__(self, max_slots: int, output_slots:int, input_slots: List[InputSlot]):
        self.max_slots = max_slots
        self.__validate_input_slots(input_slots)
        self.input_slots = input_slots
        self.item_slot_mapping = {}
        self.beverages_ingredients_mapping = {}
        self.output_slots = output_slots

    def __validate_input_slots(self, input_slots):
        # all the input slots are present
        if len(input_slots) > self.max_slots:
            raise Exception(f"Input slots{len(input_slots)} are more than the allowed slots{self.max_slots} of this machine!!")

        # check if an input slot name is not repeated

    def add_item(self, item: Item):
        unique_name = item.name
        if unique_name in self.item_slot_mapping:
            raise Exception(f"slot {item.input_slot.name} is already assigned an item {item.name}")
        # One item to one slot
        self.item_slot_mapping[unique_name] = item

    def add_beverage(self, beverage: Beverage):
        if beverage.name in self.beverages_ingredients_mapping:
            raise Exception(f"Beverage {beverage.name} already added to the coffee machine")

        ingredients = beverage.ingredients
        diff_ing = set(ingredients.keys()) - set(self.item_slot_mapping.keys())
        if len(diff_ing) > 0:
            # This means some items in beverage ingredients doesn't exist in coffee machine
            # like for hot chocolate beverage --> chocolate syrup is not present in coffee machine
            raise Exception(f"Unsupported item {diff_ing} in ingredients for the beverage {beverage.name}, coffee machine have only these items: {self.item_slot_mapping.keys()}")

        # print(ingredients)
        error_for_req_cap = []
        for ing_name, req_cap in ingredients.items():
            if self.item_slot_mapping[ing_name].filled < req_cap:
                error_for_req_cap.append((ing_name, req_cap, self.item_slot_mapping[ing_name].filled))

        if error_for_req_cap:
            raise Exception(f"Requirements {error_for_req_cap[0]}, {error_for_req_cap[1]} can't be met by the machine, allowed: {error_for_req_cap[2]}!!")

        if len(self.beverages_ingredients_mapping.keys()) + 1> self.output_slots:
            raise Exception(f"Only {self.output_slots} many beverages allowed!!!")
        self.beverages_ingredients_mapping[beverage.name] = beverage

    def __check_ingredients_available(self, beverage):

        for ing, cap in beverage.ingredients.items():
            if cap > self.item_slot_mapping[ing].filled:
                raise Exception(f"{beverage.name} cannot be prepared because item {ing} is not sufficient")

    def __subtract_required_amount(self, beverage):
        for ing, cap in beverage.ingredients.items():
            self.item_slot_mapping[ing].filled -= cap

    def request_beverage(self, beverage: str):
        if beverage not in self.beverages_ingredients_mapping.keys():
            raise Exception(f"beverage {beverage} not supported because it doesn't exists in the coffee machine {self.beverages_ingredients_mapping.keys()}!!")
        # check for ingredients capacity
        # subtract required amount
        with lock:
            self.__check_ingredients_available(self.beverages_ingredients_mapping[beverage])
            self.__subtract_required_amount(self.beverages_ingredients_mapping[beverage])

        # prepare beverage
        # serve beverage
        print(f"{beverage} is prepared")

    def refill_item(self, item_name, cap):
        if item_name not in self.item_slot_mapping.keys():
            raise Exception(f"Wrong item name {item_name} It is not assigned any slot!!")

        self.item_slot_mapping[item_name].refill(cap)

    # just for debugging
    def check_items_current_capacity(self):
        for item_name, item in self.item_slot_mapping.items():
            print(item_name, item.filled)
