# module convert
"""
Contains functions for converting from CSV to JSON and vice versa.
"""

import csv
import json

def json_to_csv(file_name: str) -> None:
    """
    Writes to a new CSV file with the specified name given a JSON file with the same name.
    """

    csv_file_path:  str = f"../data/{file_name}.csv"
    json_file_path: str = f"../data/{file_name}.json"

    try:
        with open(json_file_path, mode='r', encoding="utf-8") as json_file:
            json_data: list[dict] = json.load(json_file)

        with open(csv_file_path, mode='w', encoding="utf-8", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            csv_writer.writerow(json_data[0].keys())

            for item in json_data:
                csv_writer.writerow(item.values())

    except FileNotFoundError as e:
        raise e

def csv_to_json(file_name: str) -> None:
    """
    Writes to a new JSON file with the specified name given a CSV file with the same name.
    """

    json_data: list[dict] = []

    csv_file_path:  str = f"../data/{file_name}.csv"
    json_file_path: str = f"../data/{file_name}.json"

    with open(csv_file_path, mode='r', encoding="utf-8") as csv_file:
        csv_data: csv.DictReader = csv.DictReader(csv_file)

        for row in csv_data:
            json_data.append(row)

    with open(json_file_path, mode='w', encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4)
