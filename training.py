import pickle

from player import QLearningPlayer
from enum_list import SquareState
from board import BoardGame


folder = "C:\\Users\\Admin\\PycharmProjects\\xs_and_os\\training_folder\\"
q_table_file = folder + "q_table.okl"

def save_q_table(q_table_values, filename):
    with open(filename, "wb") as file:
        pickle.dump(q_table_values, file)


def load_q_table(filename):
    try:
        with open(filename, "rb") as file:
            q_table_values = pickle.load(file)

    except FileNotFoundError:
        q_table_values = {}
    return q_table_values


q_table_1 = load_q_table(q_table_file+"1")
q_table_2 = load_q_table(q_table_file+"2")
computer = QLearningPlayer(SquareState.O)
computer_2 = QLearningPlayer(SquareState.X)

computer.set_q_table(q_table_1)
computer_2.set_q_table(q_table_2)



players = [computer, computer_2]


for game in range(10000):
    game_running = True
    turn = 0
    winner = ""
    board = BoardGame()

    # more in depth history
    history = [[], []]
    while game_running:

        player = players[turn]

        state = board.get_state()
        move = player.choose_move(board)

        if move is not None:
            board.make_move(move, player.symbol)
        next_state = board.get_state()
        history[turn].append((state, move, next_state))


        result = board.check_win()

        # Game has ended
        if result is not None:
            if result == "Draw":
                rewards = [0, 0]

            else:
                rewards = [-1, -1]
                rewards[turn] = 1 # combination just makes the loser have -1 and current player (winner) 1.

            # learn backwards through the move's made by each player
            for i in range(2):

                history_player = history[i]
                next_reward = rewards[i]

                for state, move, next_state in reversed(history_player):
                    players[i].learn(state, move, next_reward, next_state, board)
                    next_reward = 0


            game_running = False
        else:
            # switch player
            turn = (turn + 1) % 2
computer.save_q_table(q_table_file + "1")
computer_2.save_q_table(q_table_file+"2")


with open(q_table_file + "1", "rb") as file:
    q_table = pickle.load(file)

for state, moves in list(q_table.items())[:5]:
    print(state, moves)

print("Number of states:", len(q_table))

for state, moves in list(q_table.items())[:10]:
    print("State:", state)
    print("Moves:", moves)
    print()