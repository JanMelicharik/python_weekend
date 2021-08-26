from datetime import datetime
from typing import List, Dict


def read_time_string(time_str: str) -> datetime:
    """Parse time from ISO like format to datetime object.

    :argument time_str:
    :return: datetime
    """
    return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")


def generate_flight_id(flight_details: dict) -> str:
    """ Generate flight ID from the origin, destination airport codes
    and departure and arrival times.

    :param flight_details: Dictionary with flight details.
    :return: flight ID
    """
    departure_str = flight_details["departure"].strftime("%Y%m%d%H%M")
    arrival_str = flight_details["arrival"].strftime("%Y%m%d%H%M")
    return (
        f"{flight_details['origin']}"
        f"{departure_str}"
        f"{flight_details['destination']}"
        f"{arrival_str}"
    )


def format_results(results: List[Dict]) -> List[Dict]:
    return sorted(results, key=lambda item: item["total_price"])


def get_layover(first_flight, second_flight) -> float:
    """Compute layover in hours between two flights.

    :param first_flight:
    :param second_flight:
    :return: Layover in hours
    """
    return (first_flight["arrival"] - second_flight["departure"]).seconds / 3600
