# pylint: disable=invalid-name
"""
Module to convert numbers from a file to Binary and Hexadecimal.
This program adheres to PEP-8 standards and avoids external libraries
for conversion functions like bin() or hex().
"""

import sys
import time
import os

def read_file(file_path):
    """
    Reads a file and returns a list of valid numbers.
    Skips invalid data and prints an error message for each bad item.
    """
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    # Treat numbers as integers/floats
                    number = int(float(line))
                    data.append(number)
                except ValueError:
                    print(f"Error: Invalid data at line {line_num}: '{line}'")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

    return data

def to_binary(n):
    """
    Converts a number to its binary representation string.
    Uses basic algorithms.
    """
    if n == 0:
        return "0"
    binary_str = ""
    is_negative = False
    if n < 0:
        is_negative = True
        n = abs(n)
    while n > 0:
        remainder = n % 2
        binary_str = str(remainder) + binary_str
        n = n // 2
    if is_negative:
        binary_str = "-" + binary_str
    return binary_str

def to_hexadecimal(n):
    """
    Converts a number to its hexadecimal representation string.
    Uses basic algorithms.
    """
    if n == 0:
        return "0"
    hex_map = "0123456789ABCDEF"
    hex_str = ""
    is_negative = False
    if n < 0:
        is_negative = True
        n = abs(n)
    while n > 0:
        remainder = n % 16
        hex_str = hex_map[remainder] + hex_str
        n = n // 16
    if is_negative:
        hex_str = "-" + hex_str
    return hex_str

def save_results_to_file(results):
    """
    Saves the list of result strings to a file.
    Handles the directory logic to save in 'results' if it exists.
    """
    output_path = "ConvertionResults.txt"

    # Try to put it in results folder if it exists in current dir
    if os.path.exists("results") and os.path.isdir("results"):
        output_path = os.path.join("results", "ConvertionResults.txt")

    try:
        with open(output_path, "w", encoding='utf-8') as f:
            for line in results:
                f.write(line + "\n")
        print(f"\nResults saved to {output_path}")
    except IOError as e:
        print(f"Error writing to file: {e}")

def main():
    """
    Main function to execute conversion and handle I/O.
    """
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py <fileWithData.txt>")
        sys.exit(1)

    input_filename = sys.argv[1]
    start_time = time.time()

    data = read_file(input_filename)
    if data is None:
        sys.exit(1)

    # Prepare output content
    results = []
    header = f"{'ITEM':<5} | {'NUMBER':<10} | {'BINARY':<20} | {'HEX':<20}"
    separator = "-" * 60

    print(header)
    print(separator)
    results.append(header)
    results.append(separator)

    for i, num in enumerate(data, 1):
        b_val = to_binary(num)
        h_val = to_hexadecimal(num)
        line_str = f"{i:<5} | {num:<10} | {b_val:<20} | {h_val:<20}"
        print(line_str)
        results.append(line_str)

    elapsed = time.time() - start_time
    time_msg = f"\nTime elapsed: {elapsed:.6f} seconds"
    print(time_msg)
    results.append(time_msg)

    # Save to file using helper function
    save_results_to_file(results)

if __name__ == "__main__":
    main()
