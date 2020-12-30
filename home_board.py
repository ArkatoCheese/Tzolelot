from direction import Direction
from protocol_message_handler import Status
from math import sqrt

X = 0
Y = 1
DIRECTION_TO_VALUES = {Direction.RIGHT: (1, 0), Direction.DOWN: (0, 1),
                       Direction.LEFT: (-1, 0), Direction.UP: (0, -1)}


class HomeBoard:
    def __init__(self, width, height):
        self.submarines = []
        self.width = width
        self.height = height

    def add_submarine(self, submarine):
        self.submarines.append(submarine)

    def hit_at_location(self, location):
        for submarine in self.submarines:
            if submarine.is_within_submarine(location):
                submarine.hit_location(location)
                if self.is_board_done():
                    return Status.VICTORY
                if submarine.was_sunk():
                    return Status.FULL_SUB
                return Status.CORRECT
        return Status.INCORRECT

    def is_board_done(self):
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
        final_location = (self.start_location[X] + direction_values[X]*(self.size - 1),
                          self.start_location[Y] + direction_values[Y]*(self.size - 1))
        return distance_between_two_points(self.start_location, location) + \
            distance_between_two_points(location, final_location) == \
            distance_between_two_points(self.start_location, final_location)

    def hit_location(self, location):
        if location in self.hit_locations:
            return
        self.hit_locations.append(location)

    def was_sunk(self):
        return len(self.hit_locations) == self.size


def distance_between_two_points(first_point, second_point):
    return sqrt((first_point[X] - second_point[X])**2 + (first_point[Y] - second_point[Y])**2)
