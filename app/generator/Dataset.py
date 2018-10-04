from aenum import MultiValueEnum


class Dataset(MultiValueEnum):
    HOTEL = 1, 'data/hotel.csv'
    PREDATOR = 2, 'data/predator.csv'
    # CELL = 3, 'data/cell.json'

    def __init__(self, index, path):
        self.index = index
        self.path = path
