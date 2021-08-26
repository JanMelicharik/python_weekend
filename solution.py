from helpers.input_validation import read_criteria
from helpers import loader
from helpers.search import RouteMaster

# [X] Load data
# [X] Parse data
# [ ] Create a graph
# [ ] Run algorithm (Depth first search) - Find all routes between A and B
# [ ] Sort results
# [ ] Write README

# Input validation:
# a) Compare number of requested bags to the highest number of available bags.
# b) Check if the airport is ok (no numbers, exactly 3 letters)
# c) Should not depend whether is in capitals or mixed or lowercase

# Conditions for creating a graph:
# 1. Layover between 1 and 6 hours - inclusive
# 2. Number of bags by request

# Additional features:
# - Number of passengers
# - Return flight
# - Max price
# - Max duration if trip (in hours) - should be able to understand that 1.5 hours is 90 minutes
# - Duration of stay

# Way of creating a graph:
# Each flight is a node and based on connection criteria


def main():
    criteria = read_criteria()
    flights = loader.load_data(criteria.data)

    route_master = RouteMaster(criteria, flights)
    single_flight_connections = route_master.single_flight_search()



if __name__ == '__main__':
    main()
