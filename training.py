import pickle

from player import QLearningPlayer
from enum_list import SquareState
from board import BoardGame


folder = "C:\\Users\\Admin\\PycharmProjects\\xs_and_os\\training_folder\\"
computer = QLearningPlayer(SquareState.O)
computer_2 = QLearningPlayer(SquareState.X)

computer.load_q_table(folder + "q_table.okl")
computer_2.load_q_table(folder + "q_table.okl")

board = BoardGame()

players = [computer, computer_2]
game_running = True
turn = 0
winner = ""

while game_running:
    player = players[turn]

    state = board.get_state()
    move = player.choose_move(board)

    if move is not None:
        board.make_move(move, player.symbol)

    next_state = board.get_state()
    result = board.check_win()
    if board.check_win() is not None:
        if result == "Draw":
            game_running = False
            for player in players:
                player.learn(state, move, 0, next_state, board)
        else:
            game_running = False
            winner = player.symbol
            reward = 1
            player.learn(state, move, reward, next_state, board)

            loser = players[(turn + 1) % 2]
            loser.learn(state, move, -1, next_state, board)
        computer.save_q_table(folder + "q_table.okl")
        computer_2.save_q_table(folder + "q_table.okl")
    else:
        turn = (turn + 1) % 2



with open(folder + "q_table.okl", "rb") as file:
    q_table = pickle.load(file)

for state, moves in list(q_table.items())[:5]:
    print(state, moves)

print("Number of states:", len(q_table))