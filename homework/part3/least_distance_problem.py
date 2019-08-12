#! /usr/bin/python
# -*- coding: utf-8 -*-
import random
from functools import lru_cache, wraps
import math
import time

connection_graph = {}


def get_call_time(func):
    @wraps(func)
    def _inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("function called time is : {}".format(time.time() - start))
        return result

    return _inner


@lru_cache(maxsize=2 ** 10)
def search(start, connections):
    global connection_graph
    if len(connections) == 0:
        return 0

    candidates = []
    connection_list = connections.split(",")
    for node in connection_list:
        distance = geo_distance(connection_graph[start], connection_graph[node])
        other_nodes = [item for item in connection_list if item != node]
        path_distance = distance + search(node, ",".join(other_nodes))
        candidates.append(path_distance)

    min_distance = min(candidates)
    return min_distance


@lru_cache(maxsize=2 ** 10)
def geo_distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)
    Returns
    -------
    distance_in_km : float

    Examples
    --------
     origin = (48.1372, 11.5756)  # Munich
     destination = (52.5186, 13.4083)  # Berlin
     round(distance(origin, destination), 1) 504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d


def main():
    platitudes = [random.randint(-100, 100) for _ in range(10)]
    longitude = [random.randint(-100, 100) for _ in range(10)]
    start = (random.randint(-100, 100), random.randint(-100, 100))
    connection_graph["0"] = start
    for i in range(len(platitudes)):
        connection_graph[str(i + 1)] = (longitude[i], platitudes[i])

    print(search("0", ",".join([str(item) for item in sorted(list(range(1, len(platitudes) + 1)))])))


if __name__ == '__main__':
    main()
