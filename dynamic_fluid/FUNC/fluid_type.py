# from enum import Enum
from . import fluid

class Fluid:
    def __init__(self, value):
        self.value = value

Water = Fluid(fluid.type.entity.water)
Air = Fluid(fluid.type.entity.air)