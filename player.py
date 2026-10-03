from enum_list import *


class Player:
    def __init__(self, game, player_type, symbol):
        self.game = game
        self.type = player_type
        self.symbol = symbol

    def set_player_type(self, player_type):
        self.type = player_type

    def move(self, board):
        if self.type == PlayerType.COMPUTER:
            for square in board.squares.values():
                if square.symbol == SquareState.Empty:
                    square.change_state(self.symbol)
                    return

    def set_symbol(self, symbol):
        self.symbol = symbol
