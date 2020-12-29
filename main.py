import socket
from connection_handler import ConnectionHandler
from protocol_message_handler import ProtocolMessagesHandler
from home_board import HomeBoard, Direction, Submarine
import sys


PORT = 3000
IP = "127.0.0.1"
VERSION = "1.0"


class BattleshipGame:
    def __init__(self, connection_handler, protocol_message_handler, home_board, away_board):
        self.connection_handler = connection_handler
        self.protocol_handler = protocol_message_handler
        self.home_board = home_board
        self.away_board = away_board

    def guess_battleship_location(self, location):
        self.connection_handler.send_message(self.protocol_handler.get_attempt_message(location))
        return self.protocol_handler.parse_answer_message(self.connection_handler.receive_message())

    def answer_battleship_guess(self):
        attempt = self.connection_handler.receive_message()
        location = self.protocol_handler.parse_attempt_message(attempt)
        status = self.home_board.hit_at_location(location)
        self.connection_handler.send_message(self.protocol_handler.get_answer_message(status, location))


def connect_to_opponent():
    connection = socket.socket()
    connection.connect((IP, PORT))
    return connection


def wait_for_opponent_to_connect():
    connection = socket.socket()
    connection.bind((IP, PORT))
    connection.listen(1)
    client_connection, address = connection.accept()
    return client_connection


def main():
    if len(sys.argv) > 1:
        connection = connect_to_opponent()
        my_turn = True
    else:
        connection = wait_for_opponent_to_connect()
        my_turn = False
    connection_handler = ConnectionHandler(connection)
    protocol_handler = ProtocolMessagesHandler(VERSION)
    home_board = HomeBoard()
    home_board.add_submarine(Submarine((0, 0), 3, Direction.RIGHT))
    battleship_game = BattleshipGame(connection_handler, protocol_handler, home_board, None)
    if my_turn:
        battleship_game.guess_battleship_location((1, 0))
    else:
        battleship_game.answer_battleship_guess()


if __name__ == "__main__":
    main()
