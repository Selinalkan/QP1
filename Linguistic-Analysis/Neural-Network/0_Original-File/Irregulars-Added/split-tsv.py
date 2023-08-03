#!/usr/bin/env python

import os
import random

def read_tsv_file(input_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    return lines

def shuffle_rows(data):
    random.shuffle(data)

def split_tsv_file(input_file, output_folder, num_splits):
    # Read the original TSV file and shuffle the rows
    data = read_tsv_file(input_file)
    shuffle_rows(data)

    # Calculate the number of rows per split and the number of remaining rows
    rows_per_split = len(data) // num_splits
    remaining_rows = len(data) % num_splits

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Write the shuffled rows to the output TSV files
    current_row = 0
    for i in range(num_splits):
        output_file_path = os.path.join(output_folder, f"mri_{i+1}.tsv")
        with open(output_file_path, 'w') as outfile:
            # Determine the number of rows for the current split
            num_rows = rows_per_split + 1 if i < remaining_rows else rows_per_split

            # Write the rows to the current output file
            outfile.writelines(data[current_row:current_row + num_rows])

            # Move the current_row pointer to the next set of rows
            current_row += num_rows

if __name__ == "__main__":
    input_file = "mri-lemma-passive.tsv"
    output_folder = "Split-Files"
    num_splits = 10

    split_tsv_file(input_file, output_folder, num_splits)




