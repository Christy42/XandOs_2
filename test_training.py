import pickle

from player import QLearningPlayer, RandomPlayer
from enum_list import SquareState
from board import BoardGame


folder = "C:\\Users\\Admin\\PycharmProjects\\xs_and_os\\training_folder\\"
q_table_file = folder + "q_table.okl"
interesting_game_file = folder + "interesting_games.txt"

def record_game(result, history, filename):
    if result not in ("Draw", "Loss"):
        return

    with open(filename, "a") as file:
        file.write(f"\n{'=' * 50}\n")
        file.write(f"{result}\n")
        file.write(f"{'=' * 50}\n")

        for move_number, (symbol, move, info) in enumerate(history, start=1):

            file.write(
                f"\nMove {move_number}: {symbol} -> {move}\n"
            )

            if info is not None:
                q_values = info["q_values"]
                chosen_move = info["chosen_move"]

                sorted_moves = sorted(
                    q_values.items(),
                    key=lambda item: item[1],
                    reverse=True
                )

                file.write("Q-values:\n")

                for coord, value in sorted_moves:
                    marker = " <-- CHOSEN" if coord == chosen_move else ""
                    file.write(
                        f"    {coord}: {value:.4f}{marker}\n"
                    )


def load_q_table(filename):
    try:
        with open(filename, "rb") as file:
            q_table_values = pickle.load(file)

    except FileNotFoundError:
        q_table_values = {}
    return q_table_values


q_table_1 = load_q_table(q_table_file+"1")
q_table_2 = load_q_table(q_table_file+"2")
computer = QLearningPlayer(SquareState.O, epsilon=0)
computer.set_q_table(q_table_1)
# computer = RandomPlayer(SquareState.O)


computer_2 = RandomPlayer(SquareState.X)
# computer_2 = QLearningPlayer(SquareState.X, epsilon=0)
# computer_2.set_q_table(q_table_2)


players = [computer, computer_2]

results = {SquareState.O: 0, SquareState.X: 0, "Draw": 0}
for game in range(10000):
    game_running = True
    turn = 0
    winner = ""
    board = BoardGame()
    history = []

    # more in depth history
    while game_running:

        player = players[turn]

        move = player.choose_move(board)

        if move is not None:
            board.make_move(move, player.symbol)
        if isinstance(player, QLearningPlayer):
            history.append((
                player.symbol,
                move,
                player.last_move_info
            ))
        else:
            history.append((
                player.symbol,
                move,
                None
            ))
        result = board.check_win()

        if result is not None:
            game_running = False
            results[result] += 1
            if result == "Draw":
                record_game("Draw", history, interesting_game_file)
            elif result == SquareState.X:
                record_game("Loss", history, interesting_game_file)

        turn = (turn + 1) % 2

for result in results:
    print(str(result) + ": " + str(results[result]))
