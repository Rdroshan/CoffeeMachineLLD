from enum import Enum


class Unit(Enum):
    ML = "ml"


class InputSlot:
    def __init__(self, name, capacity, unit):
        self.name = name
        self.capacity = capacity
        if unit not in [Unit.ML.value]:
            raise Exception(f"unit {unit} not supported!!")
        self.unit = unit
