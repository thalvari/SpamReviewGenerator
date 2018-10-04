from enum import Enum


class Dataset(Enum):
    HOTEL = 'datasets/hotel.csv'
    PREDATOR = 'datasets/predator.csv'
    CELL = 'datasets/cell.json'

    def __init__(self, path):
        self.path = path
