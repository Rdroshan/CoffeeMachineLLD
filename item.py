
from input_slot import InputSlot


class Item:

    def __init__(self, name, filled, input_slot: InputSlot):
        # filled tracks how much currently the ingredient is available
        self.filled = filled
        if filled > input_slot.capacity:
            print(f"Filled ingredient {filled} more than the capacity of the slot!!")
            self.filled = input_slot.capacity
        self.input_slot = input_slot
        self.name = name

    def refill(self, cap):
        new_cap = cap + self.filled
        if new_cap > self.input_slot.capacity:
            print(f"Filled ingredient {new_cap} more than the capacity of the slot!!")
            self.filled = self.input_slot.capacity
        self.filled = new_cap
