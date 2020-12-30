import socket
from connection_handler import ConnectionHandler
from protocol_message_handler import ProtocolMessagesHandler, Status
from home_board import HomeBoard, Direction, Submarine, DIRECTION_TO_VALUES, X, Y
from away_board import AwayBoard
import sys


PORT = 3000
IP = "127.0.0.1"
VERSION = "1.0"
AVAILABLE_SUBMARINE_SIZES = [2, 2, 3, 3, 4, 5]
WIDTH = 10
HEIGHT = 10
NO_SUBMARINE = "-"
SUBMARINE = "@"
BOMBED_SUBMARINE = "*"


class BattleshipGame:
    def __init__(self, connection_handler, protocol_message_handler, home_board, away_board):
        self.connection_handler = connection_handler
        self.protocol_handler = protocol_message_handler
        self.home_board = home_board
        self.away_board = away_board

    def guess_battleship_location(self, location):
        self.connection_handler.send_message(self.protocol_handler.get_attempt_message(location))
        result = self.protocol_handler.parse_answer_message(self.connection_handler.receive_message())
        if result != Status.INCORRECT:
            self.away_board.set_hit_at(location[X], location[Y])
        else:
            self.away_board.set_miss_at(location[X], location[Y])
        return result

    def answer_battleship_guess(self):
        attempt = self.connection_handler.receive_message()
        location = self.protocol_handler.parse_attempt_message(attempt)
        print(f"Opponent tried to bomb at {location}")
        status = self.home_board.hit_at_location(location)
        self.connection_handler.send_message(self.protocol_handler.get_answer_message(status, location))


def connect_to_opponent(protocol_handler):
    connection = socket.socket()
    connection.connect((IP, PORT))
    connection_handler = ConnectionHandler(connection)
    connection_handler.send_message(protocol_handler.get_ready_message())
    protocol_handler.parse_ready_message(connection_handler.receive_message())
    return connection_handler


def wait_for_opponent_to_connect(protocol_handler):
    connection = socket.socket()
    connection.bind((IP, PORT))
    connection.listen(1)
    client_connection, address = connection.accept()
    connection_handler = ConnectionHandler(client_connection)
    connection_handler.send_message(protocol_handler.get_ready_message())
    protocol_handler.parse_ready_message(connection_handler.receive_message())
    return connection_handler


def print_away_board(away_board):
    print("Away board: ")
    for i in range(away_board.width):
        temp_buffer = ""
        for j in range(away_board.height):
            temp_buffer += away_board.board[j][i]
        print(temp_buffer)


def print_home_board(home_board):
    print("Home board: ")
    board = [[NO_SUBMARINE for _ in range(home_board.height)] for _ in range(home_board.width)]
    for submarine in home_board.submarines:
        for i in range(submarine.size):
            x_value = submarine.start_location[X] + i * DIRECTION_TO_VALUES[submarine.direction][X]
            y_value = submarine.start_location[Y] + i * DIRECTION_TO_VALUES[submarine.direction][Y]
            board[x_value][y_value] = BOMBED_SUBMARINE if (x_value, y_value) in submarine.hit_locations else SUBMARINE
    for i in range(home_board.height):
        temp_buffer = ""
        for j in range(home_board.width):
            temp_buffer += board[j][i]
        print(temp_buffer)


def get_submarine_from_user(available_submarine_sizes, home_board):
    print_home_board(home_board)
    print(f"Available submarines: {available_submarine_sizes}")
    x_value = input("Give an X value for the submarine\n")
    y_value = input("Give a Y value for the submarine\n")
    size = input("What will be the size of this submarine?\n")
    direction = input("What will be the direction of the submarine?")
    available_submarine_sizes.remove(int(size))
    return Submarine((int(x_value), int(y_value)), int(size), Direction.__members__[direction])


def init_board_from_user():
    home_board = HomeBoard(WIDTH, HEIGHT)
    available_submarine_sizes = AVAILABLE_SUBMARINE_SIZES[:]
    while len(available_submarine_sizes) != 0:
        submarine = get_submarine_from_user(available_submarine_sizes, home_board)
        home_board.add_submarine(submarine)
    return home_board


def get_location_from_user():
    x_value = input("Insert x value for guess\n")
    y_value = input("Insert y value for guess\n")
    return int(x_value), int(y_value)


def game_loop(battleship_game, my_turn):
    game_on = True
    while game_on:
        print_home_board(battleship_game.home_board)
        print_away_board(battleship_game.away_board)
        if my_turn:
            if battleship_game.guess_battleship_location(get_location_from_user()) == Status.VICTORY:
                game_on = False
        else:
            print("Waiting for opponent to send bombing location")
            if battleship_game.answer_battleship_guess() == Status.VICTORY:
                game_on = False
        my_turn = not my_turn


def init_default_board():
    home_board = HomeBoard(WIDTH, HEIGHT)
    home_board.add_submarine(Submarine((0, 0), 5, Direction.DOWN))
    return home_board


def main():
    home_board = init_default_board()
    away_board = AwayBoard(WIDTH, HEIGHT)
    protocol_handler = ProtocolMessagesHandler(VERSION)
    if len(sys.argv) > 1:
        connection_handler = connect_to_opponent(protocol_handler)
        my_turn = True
    else:
        connection_handler = wait_for_opponent_to_connect(protocol_handler)
        my_turn = False
    battleship_game = BattleshipGame(connection_handler, protocol_handler, home_board, away_board)
    game_loop(battleship_game, my_turn)


if __name__ == "__main__":
    main()
