import pickle


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
        self.state_mapping = {3: 0, SquareState.X: 1, SquareState.O: 2}
        self.last_move_info = {}

    def get_state(self, board):
        state = board.get_state()
        state = tuple(
            3 if square == 3
            else 1 if square == self.state_mapping[self.symbol]
            else 2
            for square in state
        )
        return state

    def choose_move(self, board):

        state = self.get_state(board)

        if state not in self.q_table:
            self.q_table[state] = {
                coord: 0.0
                for coord in board.get_empty_squares()
            }

        q_values = self.q_table[state]

        if random() < self.epsilon:
            move = choice(list(q_values.keys()))
        else:
            max_value = max(q_values.values())



            best_moves = [
                coord
                for coord, value in q_values.items()
                if value == max_value
            ]

            move = choice(best_moves)
        self.last_move_info = {
            "state": state,
            "q_values": q_values.copy(),
            "chosen_move": move
        }
        return move

    def learn(self, state, action, reward, next_state):

        if state not in self.q_table:
            self.q_table[state] = {}

        if action not in self.q_table[state]:
            self.q_table[state][action] = 0.0

        if next_state in self.q_table and self.q_table[next_state]:
            max_next_value = max(self.q_table[next_state].values())
        else:
            max_next_value = 0.0

        old_value = self.q_table[state][action]

        new_value = old_value + self.learning_rate * (
                reward + self.discount * max_next_value - old_value
        )

        self.q_table[state][action] = new_value

    def save_q_table(self, filename):

        with open(filename, "wb") as file:
            pickle.dump(self.q_table, file)

    def load_q_table(self, filename):

        try:
            with open(filename, "rb") as file:
                self.q_table = pickle.load(file)

        except FileNotFoundError:
            self.q_table = {}

    def set_q_table(self, q_table):
        self.q_table = q_table


class PerfectPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.type = PlayerType.COMPUTER
        self.last_move_score = None

    def choose_move_old(self, board):
        best_move = None
        best_score = float("-inf")
        for move in self.get_available_moves(board):

            board.squares[move].symbol = self.symbol

            score = self.minimax(board, False)

            board.squares[move].symbol = SquareState.Empty

            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def choose_move(self, board):
        best_move = None
        best_score = float("-inf")

        for move in self.get_available_moves(board):
            board.squares[move].symbol = self.symbol

            score = self.minimax(board, False)

            board.squares[move].symbol = SquareState.Empty

            if score > best_score:
                best_score = score
                best_move = move

        self.last_move_score = best_score
        return best_move

    def minimax(self, board, is_maximizing):
        winner = self.get_winner(board)

        if winner == self.symbol:
            return 1

        if winner is not None:
            return -1

        if not self.get_available_moves(board):
            return 0

        opponent = (
            SquareState.O
            if self.symbol == SquareState.X
            else SquareState.X
        )

        if is_maximizing:
            best_score = float("-inf")
            symbol = self.symbol
        else:
            best_score = float("inf")
            symbol = opponent

        for move in self.get_available_moves(board):
            board.squares[move].symbol = symbol

            score = self.minimax(board, not is_maximizing)

            board.squares[move].symbol = SquareState.Empty

            if is_maximizing:
                best_score = max(best_score, score)
            else:
                best_score = min(best_score, score)

        return best_score

    def get_available_moves(self, board):

        return [
            position
            for position, state in board.squares.items()
            if state.symbol == SquareState.Empty
        ]

    def get_winner(self, board):
        for combo in board.winning_combo:
            states = [
                board.squares[position].symbol
                for position in combo
            ]

            if states[0] != SquareState.Empty and len(set(states)) == 1:
                return states[0]

        return None
