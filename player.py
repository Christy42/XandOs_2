from enum_list import PlayerType, SquareState
from random import choice, random


class Player:

    def __init__(self, symbol):
        self.symbol = symbol
        self.type = None

    def choose_move(self, board):
        return None

class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.type = PlayerType.USER



class RandomPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.type = PlayerType.COMPUTER

    def choose_move(self, board):
        return choice(board.get_empty_squares())


class QLearningPlayer(Player):

    def __init__(
        self,
        symbol,
        learning_rate=0.1,
        discount=0.9,
        epsilon=0.1
    ):
        super().__init__(symbol)
        self.type = PlayerType.COMPUTER
        self.learning_rate = learning_rate
        self.discount = discount
        self.epsilon = epsilon

        self.q_table = {}

    def choose_move(self, board):

        state = board.get_state()

        if state not in self.q_table:
            self.q_table[state] = {
                coord: 0.0
                for coord in board.get_empty_squares()
            }

        q_values = self.q_table[state]

        if random() < self.epsilon:
            return choice(list(q_values.keys()))

        max_value = max(q_values.values())

        best_moves = [
            coord
            for coord, value in q_values.items()
            if value == max_value
        ]

        return choice(best_moves)