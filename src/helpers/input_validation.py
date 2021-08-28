import argparse
import re

from .exceptions import ValidationError


def read_criteria():
    parser = argparse.ArgumentParser(description="Travel script")

    parser.add_argument("origin", help="Three letter code of the origin airport.", type=str.lower)
    parser.add_argument("destination", help="Three letter code of the destination airport.", type=str.lower)
    parser.add_argument("--bags", required=False, help="Number of bags to include in search.", default=0, type=int)
    parser.add_argument("--return", required=False, default="false", dest="return_trip", type=asbool)
    parser.add_argument("--pax", required=False, help="Number of passengers.", default=1, type=int)
    parser.add_argument("--max-price", required=False, type=float)
    parser.add_argument(
        "--stay-duration",
        required=False,
        help="Number of days at target destination in case of return trip.",
        type=float,
        default=1
    )
    parser.add_argument(
        "--data",
        required=False,
        default=0,
        help="Data to search in (0 for data_0.csv, 3 for data_3.csv).",
        type=int
    )

    args = parser.parse_args()
    validate(args)

    return args


def asbool(value):
    """String to Boolean converter."""
    if value.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif value.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def validate(args):
    """Check whether input is valid.

    args.from - 3 letter string
    args.to - 3 letter string
    args.bags - Non negative integer
    args.pax - Integer larger than 0
    args.max_price - Non negative float

    :param args:
    :return: None
    """
    if not (re.match(r"[a-z]{3}", args.origin) and re.match(r"[a-z]{3}", args.destination)):
        raise ValidationError("Origin and Destination must be a three letter airport IATA codes.")

    if args.bags < 0:
        raise ValidationError("Number of bags cannot be negative.")

    if args.pax < 0:
        raise ValidationError("Number of passengers cannot be negative.")

    if args.max_price is not None and args.max_price <= 0:
        raise ValidationError("Maximum price cannot be zero or lower.")
