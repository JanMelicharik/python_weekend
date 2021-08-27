import csv
import sys
from typing import List, Dict
from .helpers import read_time_string

DATA_PATH = sys.path[0]


def load_data(filetype: int) -> List[Dict]:
    data = []
    filepath = f"{DATA_PATH}/data/data_{filetype}.csv"

    with open(filepath, "r") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        for line in reader:
            raw_data = {header: value for header, value in zip(header, line)}
            data.append(
                {
                    "flight_no": raw_data["flight_no"],
                    "origin": raw_data["origin"].lower(),
                    "destination": raw_data["destination"].lower(),
                    "departure": read_time_string(raw_data["departure"]),
                    "arrival": read_time_string(raw_data["arrival"]),
                    "base_price": float(raw_data["base_price"]),
                    "bag_price": float(raw_data["bag_price"]),
                    "bags_allowed": int(raw_data["bags_allowed"]),
                }
            )

    return data
