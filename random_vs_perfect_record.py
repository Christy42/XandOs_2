from collections import defaultdict
from player import RandomPlayer, PerfectPlayer
from enum_list import SquareState
from board import BoardGame


folder = "C:\\Users\\Admin\\PycharmProjects\\xs_and_os\\training_folder\\"

filename = folder + "random_vs_perfect.txt"


def get_board_string(board):
    """Return a readable representation of the current board."""
    symbols = {
        SquareState.X: "X",
        SquareState.O: "O",
        SquareState.Empty: "."
    }

    rows = []

    for y in range(1, 4):
        row = []
        for x in range(1, 4):
            square = board.squares[(x, y)]
            row.append(symbols[square.symbol])
        rows.append(" | ".join(row))

    return "\n---------\n".join(rows)


def get_opening_category(move):
    """Classify Random's first move as centre, corner or edge."""
    x, y = move

    if x == 2 and y == 2:
        return "Centre"

    if x in (1, 3) and y in (1, 3):
        return "Corner"

    return "Edge"


def record_draw(game_number, history, filename):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"\n{'=' * 50}\n")
        file.write(f"GAME {game_number}: DRAW\n")
        file.write(f"{'=' * 50}\n")

        for move_number, (symbol, move, score) in enumerate(
            history, start=1
        ):
            file.write(f"\nMove {move_number}: {symbol.name} -> {move}\n")

            if score is not None:
                file.write(f"Best minimax score: {score}\n")


# Random moves first as X; Perfect responds as O.
random_player = RandomPlayer(SquareState.X)
perfect_player = PerfectPlayer(SquareState.O)

players = [random_player, perfect_player]

results = {
    SquareState.X: 0,
    SquareState.O: 0,
    "Draw": 0
}

# Opening category -> outcome counts
opening_results = defaultdict(
    lambda: {"Perfect wins": 0, "Draws": 0, "Random wins": 0}
)

number_of_games = 1000

# Start with a fresh log for this test.
with open(filename, "w", encoding="utf-8") as file:
    file.write("Random (X) vs Perfect (O)\n")

for game in range(number_of_games):
    if game % 10 == 0:
        print(f"Game {game}/{number_of_games}")

    board = BoardGame()
    history = []
    turn = 0

    while True:
        player = players[turn]
        move = player.choose_move(board)

        if move is not None:
            board.make_move(move, player.symbol)

        score = (
            player.last_move_score
            if isinstance(player, PerfectPlayer)
            else None
        )

        history.append((player.symbol, move, score))

        board.make_move(move, player.symbol)

        history.append((
            player.symbol,
            move,
            get_board_string(board)
        ))

        result = board.check_win()

        if result is not None:
            results[result] += 1

            opening_category = get_opening_category(history[0][1])

            if result == "Draw":
                opening_results[opening_category]["Draws"] += 1
                record_draw(game + 1, history, filename)

            elif result == SquareState.O:
                opening_results[opening_category]["Perfect wins"] += 1

            elif result == SquareState.X:
                opening_results[opening_category]["Random wins"] += 1

            break

        turn = (turn + 1) % 2


print("\nOverall results")
print("-" * 40)

for result, count in results.items():
    print(f"{result}: {count} ({count / number_of_games:.2%})")

print("\nResults by Random's opening move")
print("-" * 60)

for category in ("Centre", "Corner", "Edge"):
    counts = opening_results[category]
    total = sum(counts.values())

    if total == 0:
        continue

    print(f"\n{category} ({total} games)")

    for outcome, count in counts.items():
        print(f"  {outcome}: {count} ({count / total:.2%})")

print(f"\nDetailed draw records saved to: {filename}")