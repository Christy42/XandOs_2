from game_code import BoardGame
from board import SquareState

coord_to_action = {
    (1, 1): 0,
    (1, 2): 1,
    (1, 3): 2,
    (2, 1): 3,
    (2, 2): 4,
    (2, 3): 5,
    (3, 1): 6,
    (3, 2): 7,
    (3, 3): 8,
}


class TicTacToeEnvironment:

    def __init__(self):
        self.board = BoardGame()
        self.current_player = SquareState.X
        self.ai_symbol = None
        self.opponent_symbol = None

    def reset(self):
        self.board.reset()
        self.current_player = SquareState.X
        return self.board.get_state()

    def step(self, action):
        pass

    def reward(self, winner):
        if winner == self.ai_symbol:
            reward = 1
        elif winner == self.opponent_symbol:
            reward = -1
        elif winner == SquareState.Empty:
            reward = 0
        else:
            reward = 0
        return reward