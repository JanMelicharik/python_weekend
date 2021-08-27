from datetime import datetime


def read_time_string(time_str: str) -> datetime:
    """Parse time from ISO like format to datetime object.

    :argument time_str:
    :return: datetime
    """
    return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")


def layover(later: datetime, earlier: datetime) -> float:
    """Compute layover in hours between two flights.

    :param later: Later time
    :param earlier: Earlier time
    :return: Layover in hours
    """
    return (later - earlier).seconds / 3600


def format_time_difference(later: datetime, earlier: datetime) -> str:
    """Return time difference in human-readable form.

    :param later: Later time
    :param earlier: Earlier time
    :return: Difference in time
    """
    return str(later - earlier)
