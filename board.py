from enum_list import *


class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = SquareState.Empty

    def change_state(self, new_state):
        if self.symbol == SquareState.Empty:
            self.symbol = new_state


class BoardGame:
    def __init__(self):
        self.squares = {(x, y): Square(x, y) for x in range(1, 4) for y in range(1, 4)}
        self.winning_combo = [[(1, 1), (1, 2), (1, 3)], [(2, 1), (2, 2), (2, 3)], [(3, 1), (3, 2), (3, 3)],
                   [(1, 1), (2, 1), (3, 1)], [(1, 2), (2, 2), (3, 2)], [(1, 3), (2, 3), (3, 3)],
                   [(1, 3), (2, 2), (3, 1)], [(1, 1), (2, 2), (3, 3)]]

    def update_square(self, coord, new_state):
        self.squares[coord].change_state(new_state)

    def check_win(self, print_game=False):
        for match in self.winning_combo:
            states = [self.squares[coord].symbol for coord in match]
            if all(state == states[0] and state != SquareState.Empty for state in states):
                if print_game:
                    self.print_board()
                    print("Winning combination:", match)
                    print("Winner:", states[0])

                return states[0]
        empty_cells = [a for a in self.squares if self.squares[a].symbol == SquareState.Empty]
        if len(empty_cells) == 0:
            if print_game:
                self.print_board()
                print("DRAW")
            return "Draw"
        return None

    def can_play(self, square):
        if square.symbol == SquareState.Empty:
            return True, ""
        return False, "Square already filled"

    def get_state(self):
        return tuple(
            self.squares[(x, y)].symbol.value
            for x in range(1, 4)
            for y in range(1, 4)
        )

    def get_empty_squares(self):
        return [
            coord
            for coord, square in self.squares.items()
            if square.symbol == SquareState.Empty
        ]

    def make_move(self, coord, symbol):
        square = self.squares[coord]

        if square.symbol != SquareState.Empty:
            return False

        square.change_state(symbol)
        return True

    def reset(self):
        for square in self.squares.values():
            square.symbol = SquareState.Empty

    def print_board(self):
        print("\nFinal board:")

        for y in range(1, 4):
            row = []

            for x in range(1, 4):
                square = self.squares[(x, y)]

                if square.symbol == SquareState.X:
                    symbol = "X"
                elif square.symbol == SquareState.O:
                    symbol = "O"
                else:
                    symbol = "-"

                row.append(f"{symbol} ")

            print("".join(row))

        print()
