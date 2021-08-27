from helpers.input_validation import read_criteria
from helpers import loader
from helpers.search import RouteMaster
import json

# Additional features:
# - Number of passengers
# - Return flight
# - Max price
# - Duration of stay


def main():
    criteria = read_criteria()
    flights = loader.load_data(criteria.data)

    route_master = RouteMaster(criteria, flights)
    route_master.find_routes()

    print(json.dumps(route_master.routes, indent=4))


if __name__ == '__main__':
    main()
