# pylint: disable=invalid-name
"""
Module to count the frequency of distinct words in a file.
This program adheres to PEP-8 standards and avoids external libraries.
"""

import sys
import time

def read_file(file_path):
    """
    Reads a file and returns a list of words.
    It handles basic cleaning (removing punctuation and casing).
    """
    words_list = []
    # Caracteres de puntuacion a eliminar
    punctuation = ".,;!?()[]{}\"'`:"

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                # Separamos por espacios
                raw_words = line.split()

                for word in raw_words:
                    # 1. Convertimos a minusculas
                    # 2. Quitamos puntuacion de los bordes
                    cleaned_word = word.lower().strip(punctuation)

                    # Solo agregamos si no es una cadena vacia
                    if cleaned_word:
                        words_list.append(cleaned_word)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e: # pylint: disable=broad-except
        print(f"Error reading file: {e}")
        return None

    return words_list

def count_words(words_list):
    """
    Counts the frequency of each word using a dictionary.
    """
    if not words_list:
        return {}

    frequency = {}
    for word in words_list:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

    return frequency

def main():
    """
    Main function to execute the program logic.
    """
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py <fileWithData.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    start_time = time.time()

    words = read_file(input_file)

    if words is None:
        sys.exit(1)

    word_counts = count_words(words)

    elapsed_time = time.time() - start_time

    # Ordenamos primero por Frecuencia (Mayor a menor) y luego Alfabet.
    sorted_words = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))

    # Calculamos el Gran Total
    grand_total = sum(word_counts.values())

    # Imprimir en consola y guardar en archivo
    print(f"{'Row':<5} | {'WORD':<30} | {'COUNT':<10}")
    print("-" * 50)

    with open("WordCountResults.txt", "w", encoding='utf-8') as result_file:
        # Encabezado
        result_file.write(f"{'Row':<5} | {'WORD':<30} | {'COUNT':<10}\n")
        result_file.write("-" * 50 + "\n")

        for i, (word, count) in enumerate(sorted_words, 1):
            # Formato de linea
            line = f"{i:<5} | {word:<30} | {count:<10}"

            # Pantalla
            print(line)
            # Archivo
            result_file.write(line + "\n")

        # --- SECCION DEL GRAND TOTAL ---
        separator = "-" * 50
        total_line = f"{'':<5} | {'GRAND TOTAL':<30} | {grand_total:<10}"

        # Pantalla
        print(separator)
        print(total_line)
        print(separator)
        print(f"Time elapsed: {elapsed_time:.6f} seconds")

        # Archivo
        result_file.write(separator + "\n")
        result_file.write(total_line + "\n")
        result_file.write(separator + "\n")
        result_file.write(f"Time elapsed: {elapsed_time:.6f} seconds\n")

if __name__ == "__main__":
    main()
