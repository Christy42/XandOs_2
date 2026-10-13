import pickle


folder = "C:\\Users\\Admin\\PycharmProjects\\xs_and_os\\training_folder\\"
q_table_file = folder + "q_table.okl"


with open(q_table_file + "1", "rb") as file:
    q_table = pickle.load(file)

print("Number of states:", len(q_table))
q_values = 0
num_pos, num_neg, num_zero = 0, 0, 0
for element in q_table:

    q_values += len(q_table[element])

    num_pos += len([a for a in q_table[element] if q_table[element][a] > 0])
    num_neg += len([a for a in q_table[element] if q_table[element][a] < 0])
    num_zero += len([a for a in q_table[element] if q_table[element][a] == 0])

print(type(q_table))
print("Number q values:", q_values)
print("Positive: ", num_pos)
print("Negative: ", num_neg)
print("Zero: ", num_zero)


states_with_zero = 0
states_all_zero = 0

for state, moves in q_table.items():

    if any(value == 0 for value in moves.values()):
        states_with_zero += 1

    if moves and all(value == 0 for value in moves.values()):
        states_all_zero += 1

print("States with at least one zero:", states_with_zero)
print("States with all zero values:", states_all_zero)




zero_by_empty = {}

for state, moves in q_table.items():

    if all(value == 0 for value in moves.values()):

        empty_squares = state.count(3)

        if empty_squares not in zero_by_empty:
            zero_by_empty[empty_squares] = 0

        zero_by_empty[empty_squares] += 1

print(zero_by_empty)

