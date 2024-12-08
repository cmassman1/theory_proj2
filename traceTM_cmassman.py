def parse_csv(filename):
    """Parses the NTM (Non-Deterministic Turing Machine) definition from a CSV file."""
    import os
    import csv

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

def simulate_ntm_bfs(filename, input_string, max_depth=10, max_transitions=100, output_file_path="outputfile_cmassman.txt"):
    """Simulates a Non-Deterministic Turing Machine using BFS."""
    headers, transitions = parse_csv(filename)
    machine_name = headers[0][0]
    start_state = headers[4][0]
    accept_state = headers[5][0]
    reject_state = headers[6][0]

    def write_output(message):
        """Writes output to a file and prints to console."""
        with open(output_file_path, "a") as output_file:
            output_file.write(message + '\n')
        print(message)  # Also prints to console for live tracking

    # Log initial details
    write_output(f"Processing {filename} with input: {input_string}")
    write_output(f"Machine: {machine_name}")
    write_output(f"Input string: {input_string}")

    if not input_string.strip():
        write_output("String rejected immediately: input is empty and does not satisfy the language.")
        write_output("Depth of the tree of configurations: 0")
        write_output("Total transitions simulated: 0")
        return False

    # BFS simulation initialization
    tree = [[("", start_state, input_string)]]
    total_transitions = 0
    visited_configs = set()
    accept_found = False

    def calculate_nondeterminism(tree):
        """Calculates nondeterminism as the average branching factor."""
        total_configs = sum(len(level) for level in tree)
        depth = len(tree)
        return total_configs / depth if depth > 0 else 0

    for depth in range(max_depth):
        current_level = tree[-1]
        next_level = []
        any_path_continues = False

        write_output(f"\nDepth {depth}:")
        for config in current_level:
            left, state, right = config
            total_transitions += 1
            write_output(f"[{left}], ({state}), [{right}]")

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
            nondeterminism = calculate_nondeterminism(tree)
            write_output(f"\nDepth of configuration tree: {depth + 1}")
            write_output(f"Total transitions simulated: {total_transitions}")
            write_output(f"Degree of nondeterminism: {nondeterminism:.2f}")
            write_output(f"String accepted in {depth + 1} transitions")
            return True

        if not any_path_continues:
            write_output(f"\nDepth of configuration tree: {depth + 1}")
            write_output(f"Total transitions simulated: {total_transitions}")
            write_output(f"Degree of nondeterminism: {calculate_nondeterminism(tree):.2f}")
            write_output("String rejected.")
            return False

        if depth < max_depth:
            tree.append(next_level)

    write_output("\nExecution stopped: Max depth reached.")
    write_output(f"Depth of configuration tree: {max_depth}")
    write_output(f"Total transitions simulated: {total_transitions}")
    write_output(f"Degree of nondeterminism: {calculate_nondeterminism(tree):.2f}")
    return False


def process_multiple_csv_files():
    """Processes multiple CSV files and runs the NTM simulation."""
    csv_files = [
        ("abc_star_cmassman.csv", "abcab"),
        ("abc_star_cmassman.csv", "abc"),
        ("a_plus_cmassman.csv", ""),
        ("a_plus_cmassman.csv", "aaa"),
        ("abcd_star_cmassman.csv", "adcd"),
        ("abcd_star_cmassman.csv", "abcd")
    ]

    # Clear the output file before starting
    with open("outputfile_cmassman.txt", "w") as output_file:
        output_file.write("")  # Clear any existing content

    # Run the simulations and add blank lines between outputs
    for csv_file, input_string in csv_files:
        simulate_ntm_bfs(csv_file, input_string, max_depth=10)
        with open("outputfile_cmassman.txt", "a") as output_file:
            output_file.write("\n\n")  # Adds two blank lines after each test case


# Main execution
if __name__ == "__main__":
    process_multiple_csv_files()


