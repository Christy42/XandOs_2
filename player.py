from enum_list import PlayerType
from random import choice


class Player:
    def __init__(self, game, player_type, symbol):
        self.game = game
        self.type = player_type
        self.symbol = symbol

    def set_player_type(self, player_type):
        self.type = player_type

    def move_basic(self, board):
        if self.type == PlayerType.COMPUTER:
            for coord in board.get_empty_squares():
                return board.make_move(coord, self.symbol)
        return None

    def move(self, board):
        if self.type == PlayerType.COMPUTER:
            coord = choice(board.get_empty_squares())
            return board.make_move(coord, self.symbol)
        return None


    def set_symbol(self, symbol):
        self.symbol = symbol
