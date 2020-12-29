from direction import Direction
from protocol_message_handler import Status

X = 0
Y = 1
DIRECTION_TO_VALUES = {Direction.RIGHT: (1, 0)}


class HomeBoard:
    def __init__(self):
        self.submarines = []

    def add_submarine(self, submarine):
        self.submarines.append(submarine)

    def hit_at_location(self, location):
        for submarine in self.submarines:
            if submarine.is_within_submarine(location):
                submarine.hit_location(location)
                if submarine.was_sunk():
                    return Status.FULL_SUB
                return Status.CORRECT
        return Status.INCORRECT

    def is_board_done(self, location):
        for submarine in self.submarines:
            if not submarine.was_sunk():
                return False
        return True


class Submarine:
    def __init__(self, start_location, size, direction):
        self.start_location = start_location
        self.size = size
        self.direction = direction
        self.hit_locations = []

    def is_within_submarine(self, location):
        if location in self.hit_locations:
            return True
        direction_values = DIRECTION_TO_VALUES[self.direction]
        for i in range(self.size):
            if self.start_location[X] + i * direction_values[X] == location[X] and \
               self.start_location[Y] + i * direction_values[Y] == location[Y]:
                return True
        return False

    def hit_location(self, location):
        if location in self.hit_locations:
            return
        self.hit_locations.append(location)

    def was_sunk(self):
        return len(self.hit_locations) == self.size
