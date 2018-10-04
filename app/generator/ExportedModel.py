from enum import Enum


class ExportedModel(Enum):
    HOTEL = 'models/hotel_{}_{}.json'
    PREDATOR = 'models/predator_{}_{}.json'
    CELL = 'models/cell_{}_{}.json'

    def __init__(self, path):
        self.path = path
