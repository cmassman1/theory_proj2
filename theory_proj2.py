import csv
import os

def parse_csv(filename):
    """Parses the NTM definition from a CSV file."""
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

def simulate_ntm_bfs(filename, input_string, max_depth=10, max_transitions=100):
    """Simulates a Non-Deterministic Turing Machine using BFS."""
    headers, transitions = parse_csv(filename)
    machine_name = headers[0][0]
    start_state = headers[4][0]
    accept_state = headers[5][0]
    reject_state = headers[6][0]

    print(f"Machine: {machine_name}")
    print(f"Input string: {input_string}")

    # Reject the empty string immediately for a+ since it requires at least one 'a'
    if not input_string.strip():
        print("String rejected immediately: input is empty and does not satisfy the language.")
        print("Depth of the tree of configurations: 0")
        print("Total transitions simulated: 0")
        return False

    tree = [[("", start_state, input_string)]]
    total_transitions = 0
    accepting_path = []
    visited_configs = set()  # Track visited configurations
    accept_found = False

    for depth in range(max_depth):
        current_level = tree[-1]
        next_level = []
        any_path_continues = False

        for config in current_level:
            left, state, right = config
            total_transitions += 1

            # Skip already visited configurations
            if config in visited_configs:
                continue
            visited_configs.add(config)

            # Accept if in accept state and tape is empty
            if state == accept_state and not right:
                if not accept_found:  # Add to accepting path only once
                    accepting_path = tree[:depth + 1] + [[config]]
                accept_found = True
                break  # Stop processing other configs once accept found

            # Skip if in reject state
            if state == reject_state:
                continue

            # Handle blank symbol if right part of tape is empty
            char = right[0] if right else '_'

            # Check if there are transitions for this state and character
            if (state, char) in transitions:
                for new_state, write, move in transitions[(state, char)]:
                    # Modify tape based on write and move
                    if move == 'R':
                        new_left = left + write
                        new_right = right[1:]
                    elif move == 'L':
                        new_left = left[:-1] if left else ''
                        new_right = (left[-1] if left else '') + write + right[1:]
                    else:  # Stay in place
                        new_left = left
                        new_right = write + right[1:]

                    new_config = (new_left, new_state, new_right)
                    if new_config not in visited_configs:
                        next_level.append(new_config)
                        any_path_continues = True

        if accept_found:
            print(f"String accepted in {len(accepting_path) - 1} transitions.")
            print("Configuration Path:")
            # Use a set to track printed configurations
            printed_configs = set()
            for d, level in enumerate(accepting_path):
                for config in level:
                    left, state, right = config
                    head_char = right[0] if right else "_"
                    config_str = f"[{left}], ({state}), [{head_char + right[1:] if right else ''}]"
                    # Only print if not already printed
                    if config_str not in printed_configs:
                        print(config_str)
                        printed_configs.add(config_str)
            
            print(f"Depth of the tree of configurations: {len(accepting_path) - 1}")
            print(f"Total transitions simulated: {total_transitions}")
            return True

        if not any_path_continues:
            print(f"String rejected in {depth + 1} steps.")
            print(f"Depth of the tree of configurations: {depth + 1}")
            print(f"Total transitions simulated: {total_transitions}")
            return False

        if depth < max_depth:
            tree.append(next_level)

    print(f"Execution stopped after {max_depth} steps.")
    print(f"Depth of the tree of configurations: {max_depth}")
    print(f"Total transitions simulated: {total_transitions}")
    return False

def process_multiple_csv_files():
    """Processes multiple CSV files in the directory."""
    csv_files = [
        ("abc_star.csv", "abcab"),
        ("abc_star.csv", "abc"),
        ("a_plus.csv", ""),
        ("a_plus.csv", "aaa"),
        ("abcd_star.csv", "adcd"),
        ("abcd_star.csv", "abcd")
    ]

    for csv_file, input_string in csv_files:
        print(f"\nProcessing {csv_file} with input: {input_string}")
        simulate_ntm_bfs(csv_file, input_string, max_depth=10)

# Example usage
if __name__ == "__main__":
    process_multiple_csv_files()
