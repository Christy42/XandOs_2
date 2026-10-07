from player import QLearningPlayer
from board import SquareState
from training import q_table_file



computer = QLearningPlayer(SquareState.O, epsilon=0)
computer_2 = QLearningPlayer(SquareState.X, epsilon=0)

computer.load_q_table(q_table_file + "_o")
computer_2.load_q_table(q_table_file + "_x")