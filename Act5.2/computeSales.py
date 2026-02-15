"""
This module calculates total sales from a price catalogue and a sales record.
It adheres to PEP-8 standards and includes error handling.
"""
# pylint: disable=invalid-name

import json
import sys
import time


def load_json_file(filename):
    """
    Loads a JSON file and returns its content.
    Returns None if the file is not found or contains invalid JSON.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{filename}' contains invalid JSON.")
        return None
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(f"An unexpected error occurred while reading '{filename}': {e}")
        return None


def create_price_catalogue(price_data):
    """
    Converts the price list (list of dicts) into a dictionary
    for O(1) access time.
    Key: Product title, Value: Price
    """
    catalogue = {}
    for item in price_data:
        title = item.get("title")
        price = item.get("price")
        if title and price is not None:
            catalogue[title] = price
    return catalogue


def compute_total_sales(price_catalogue, sales_data):
    """
    Computes the total cost of sales based on the price catalogue.
    Handles missing products cleanly.
    """
    total_cost = 0.0

    for sale in sales_data:
        product_name = sale.get("Product")
        quantity = sale.get("Quantity")

        if not product_name or quantity is None:
            print(f"Invalid sale data found: {sale}")
            continue

        if product_name in price_catalogue:
            price = price_catalogue[product_name]
            total_cost += price * quantity
        else:
            print(f"Error: Product '{product_name}' not found in catalogue.")

    return total_cost


def main():
    """
    Main function to execute the sales computation.
    """
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json "
              "salesRecord.json")
        sys.exit(1)

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    start_time = time.time()

    price_data = load_json_file(price_file)
    sales_data = load_json_file(sales_file)

    if price_data is None or sales_data is None:
        sys.exit(1)

    price_catalogue = create_price_catalogue(price_data)
    total_sales = compute_total_sales(price_catalogue, sales_data)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Formatting output
    result_text = (
        f"Total Sales Cost: {total_sales:.2f}\n"
        f"Execution Time: {elapsed_time:.4f} seconds"
    )

    # Print to console
    print(result_text)

    # Save to file
    with open("SalesResults.txt", "a", encoding='utf-8') as results_file:
        results_file.write(f"Processing: {sales_file}\n")
        results_file.write(result_text + "\n")
        results_file.write("-" * 30 + "\n")


if __name__ == "__main__":
    main()
