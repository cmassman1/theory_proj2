import csv
import os

# Parsing function for reading the NTM CSV file
def parse_csv(filename):
    """Parses the NTM (Non-Deterministic Turing Machine) definition from a CSV file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Error: File '{filename}' not found.")

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = [next(reader) for _ in range(7)]
        transitions = {}

        for row in reader:
            if len(row) != 5:
                raise ValueError(f"Malformed transition line: {row}")

            state, char, new_state, write, move = row
            key = (state, char.strip())

            if key not in transitions:
                transitions[key] = []
            transitions[key].append((new_state, write.strip(), move.strip()))

        return headers, transitions

# BFS simulation function
def simulate_ntm_bfs(filename, input_string, max_depth=10, max_transitions=100, output_file=None):
    """Simulates a Non-Deterministic Turing Machine using BFS."""
    headers, transitions = parse_csv(filename)
    machine_name = headers[0][0]
    start_state = headers[4][0]
    accept_state = headers[5][0]
    reject_state = headers[6][0]

    def write_output(message):
        """Writes output to a file or prints to console."""
        if output_file:
            output_file.write(message + '\n')
        else:
            print(message)

    write_output(f"Machine: {machine_name}")
    write_output(f"Input string: {input_string}")

    if not input_string.strip():
        write_output("String rejected immediately: input is empty and does not satisfy the language.")
        write_output("Depth of the tree of configurations: 0")
        write_output("Total transitions simulated: 0")
        return False

    tree = [[("", start_state, input_string)]]
    total_transitions = 0
    visited_configs = set()
    accept_found = False

    def calculate_nondeterminism(tree):
        """Calculates the nondeterminism metric based on BFS tree structure."""
        total_branches = sum(len(level) for level in tree)
        num_levels = len(tree)
        if num_levels == 0:
            return 0.0
        return round(total_branches / num_levels, 2)

    for depth in range(max_depth):
        current_level = tree[-1]
        next_level = []
        any_path_continues = False

        for config in current_level:
            left, state, right = config
            total_transitions += 1

            if config in visited_configs:
                continue
            visited_configs.add(config)

            if state == accept_state and not right:
                accept_found = True
                tree.append([config])
                break

            if state == reject_state:
                continue

            char = right[0] if right else '_'

            if (state, char) in transitions:
                for new_state, write, move in transitions[(state, char)]:
                    if move == 'R':
                        new_left = left + write
                        new_right = right[1:]
                    elif move == 'L':
                        new_left = left[:-1] if left else ''
                        new_right = (left[-1] if left else '') + write + right[1:]
                    else:
                        new_left = left
                        new_right = write + right[1:]

                    new_config = (new_left, new_state, new_right)
                    if new_config not in visited_configs:
                        next_level.append(new_config)
                        any_path_continues = True

        if accept_found:
            nondeterminism_value = calculate_nondeterminism(tree)
            interpret_nondeterminism(nondeterminism_value, write_output)
            return True

        if not any_path_continues:
            write_output(f"String rejected in {depth + 1} steps.")
            nondeterminism_value = calculate_nondeterminism(tree)
            interpret_nondeterminism(nondeterminism_value, write_output)
            return False

        if depth < max_depth:
            tree.append(next_level)

    write_output(f"Execution stopped after {max_depth} steps.")
    nondeterminism_value = calculate_nondeterminism(tree)
    interpret_nondeterminism(nondeterminism_value, write_output)
    return False

def interpret_nondeterminism(value, write_output):
    """Interprets and prints the nondeterminism level."""
    write_output(f"Nondeterminism Metric: {value}")
    if value == 1.0:
        write_output("Computation was deterministic.")
    elif value < 1.5:
        write_output("Slight nondeterministic behavior observed.")
    elif value < 3.0:
        write_output("Moderate nondeterministic exploration.")
    else:
        write_output("Highly nondeterministic computation with extensive alternative paths.")

# Processes multiple CSV files
def process_multiple_csv_files():
    csv_files = [
        ("abc_star_cmassman.csv", "abcab"),
        ("abc_star_cmassman.csv", "abc"),
        ("a_plus_cmassman.csv", ""),
        ("a_plus_cmassman.csv", "aaa"),
        ("abcd_star_cmassman.csv", "adcd"),
        ("abcd_star_cmassman.csv", "abcd")
    ]

    with open("outputfile_cmassman.txt", "w") as output_file:
        for csv_file, input_string in csv_files:
            output_file.write(f"\nProcessing {csv_file} with input: {input_string}\n")
            simulate_ntm_bfs(csv_file, input_string, max_depth=10, output_file=output_file)

# Main execution
if __name__ == "__main__":
    process_multiple_csv_files()

