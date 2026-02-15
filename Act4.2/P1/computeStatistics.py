# pylint: disable=invalid-name
"""
Module to compute descriptive statistics from a file containing numbers.
This program adheres to PEP-8 standards and avoids external libraries
for calculations.
"""

import sys
import time

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
                    number = float(line)
                    data.append(number)
                except ValueError:
                    print(f"Error: Invalid data at line {line_num}: '{line}'")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

    return data

def compute_mean(data):
    """
    Computes the arithmetic mean of a list of numbers.
    Formula: sum(x) / N
    """
    if not data:
        return 0.0

    total_sum = 0.0
    for num in data:
        total_sum += num

    return total_sum / len(data)

def compute_median(data):
    """
    Computes the median of a list of numbers.
    Requires sorting the data first.
    """
    if not data:
        return 0.0

    sorted_data = sorted(data)
    n = len(sorted_data)
    mid_index = n // 2

    if n % 2 == 1:
        return sorted_data[mid_index]

    return (sorted_data[mid_index - 1] + sorted_data[mid_index]) / 2.0

def compute_mode(data):
    """
    Computes the mode (most frequent number).
    Returns "NA" if no number repeats (max frequency is 1).
    """
    if not data:
        return "NA"

    frequency = {}
    for num in data:
        if num in frequency:
            frequency[num] += 1
        else:
            frequency[num] = 1

    max_count = 0
    mode_val = data[0]

    for num, count in frequency.items():
        if count > max_count:
            max_count = count
            mode_val = num

    if max_count == 1:
        return "NA"

    return mode_val

def compute_variance(data, mean_val):
    """
    Computes the population variance.
    Formula: sum((x - mean)^2) / N
    """
    if not data:
        return 0.0

    sum_sq_diff = 0.0
    for num in data:
        diff = num - mean_val
        sum_sq_diff += diff * diff

    return sum_sq_diff / len(data)

def compute_std_dev(variance_val):
    """
    Computes the population standard deviation.
    Formula: sqrt(variance)
    """
    return variance_val ** 0.5

def main():
    """
    Main function to execute the program logic.
    """
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py <fileWithData.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    start_time = time.time()

    data = read_file(input_file)

    if data is None or not data:
        print("No valid data found or file error.")
        sys.exit(1)

    count_val = len(data)
    mean_val = compute_mean(data)
    median_val = compute_median(data)
    mode_val = compute_mode(data)
    variance_val = compute_variance(data, mean_val)
    std_dev_val = compute_std_dev(variance_val)

    elapsed_time = time.time() - start_time

    print(f"Count: {count_val}")
    print(f"Mean: {mean_val}")
    print(f"Median: {median_val}")
    print(f"Mode: {mode_val}")
    print(f"Standard Deviation: {std_dev_val}")
    print(f"Variance: {variance_val}")
    print(f"Time elapsed: {elapsed_time:.6f} seconds")

    with open("StatisticsResults.txt", "w", encoding='utf-8') as result_file:
        result_file.write(f"Count: {count_val}\n")
        result_file.write(f"Mean: {mean_val}\n")
        result_file.write(f"Median: {median_val}\n")
        result_file.write(f"Mode: {mode_val}\n")
        result_file.write(f"Standard Deviation: {std_dev_val}\n")
        result_file.write(f"Variance: {variance_val}\n")
        result_file.write(f"Time elapsed: {elapsed_time:.6f} seconds\n")

if __name__ == "__main__":
    main()
