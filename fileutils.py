import os
import csv

DELIMITER = ";"


def parse_csv(file_path):
    data = []
    with open(file_path, "r") as csvfile:
        csvreader = csv.reader(
            csvfile, delimiter=DELIMITER, quoting=csv.QUOTE_NONNUMERIC
        )
        next(csvreader, None)  # skipping header
        for row in csvreader:
            data.append(row)
    return data
