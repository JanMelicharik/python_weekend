from src.helpers.input_validation import read_criteria
from src.helpers import loader
from src.helpers.helpers import convert_to_eur
from src.modules.local import RouteMaster
from src.modules import regiojet
from src import redis_service
import json

# Additional features:
# - Number of passengers
# - Return flight
# - Max price
# - Duration of stay


def main():
    criteria = read_criteria()
    # flights = loader.load_data(criteria.data)
    #
    # route_master = RouteMaster(criteria, flights)
    # route_master.find_routes()
    #
    # print(json.dumps(route_master.routes, indent=4))

    r_j = regiojet.Scraper(criteria.origin, criteria.destination, criteria.dep_date)
    con = r_j.get_results()
    print(json.dumps(con, indent=4))
    # redis_client = redis_service.init_redis()
    # redis_client.set("locations", json.dumps(r_j.locations_ids))
    # redis_client.delete("locations")


if __name__ == '__main__':
    main()
