#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import math
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

os.chdir("D:/work_files/pycharm_codes/nlp_assignment")


def load_data():
    beijing_subway_geo_dict = {}  # example: {"草房":[15.26,233.56],...}
    with open("homework/part2/data/beijing_subway_geo.txt", "r", encoding="utf-8") as beijing_subway_geo_file:
        for line in beijing_subway_geo_file.readlines():
            line_strip_split = line.strip().split(":")
            subway_name = line_strip_split[0]
            subway_geo = line_strip_split[1].split(",")
            beijing_subway_geo_dict[subway_name] = (float(subway_geo[0]), float(subway_geo[1]))
    beijing_subway_belong_to_line = {}  # example: {"草房":["6号线"],...}
    beijing_subway_line = {}  # example: {"6号线":["金安桥",...]}
    beijing_subway_link = {}  # example: {"朱辛庄": ["育知路",..]}
    with open("homework/part2/data/beijing_subway_line.txt", "r", encoding="utf-8") as beijing_subway_line_file:
        for line in beijing_subway_line_file.readlines():
            line_strip_split = line.strip().split(":")
            subway_line = line_strip_split[1].split(",")
            beijing_subway_line[line_strip_split[0]] = subway_line
            for beijing_subway in subway_line:
                if beijing_subway_belong_to_line.get(beijing_subway) is None:
                    beijing_subway_belong_to_line[beijing_subway] = []
                    beijing_subway_belong_to_line[beijing_subway].append(line_strip_split[0])
                else:
                    beijing_subway_belong_to_line.get(beijing_subway).append(line_strip_split[0])
            if len(subway_line) >= 2:
                for index in range(len(subway_line) - 1):
                    if beijing_subway_link.get(subway_line[index]) is None:
                        beijing_subway_link[subway_line[index]] = []
                        beijing_subway_link[subway_line[index]].append(subway_line[index + 1])
                    else:
                        beijing_subway_link[subway_line[index]].append(subway_line[index + 1])
                    if beijing_subway_link.get(subway_line[index + 1]) is None:
                        beijing_subway_link[subway_line[index + 1]] = []
                        beijing_subway_link[subway_line[index + 1]].append(subway_line[index])
                    else:
                        beijing_subway_link[subway_line[index + 1]].append(subway_line[index])
    return beijing_subway_geo_dict, beijing_subway_line, beijing_subway_belong_to_line, beijing_subway_link


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

def plt_beijing_subway_line():
    beijing_subway_geo_dict, beijing_subway_line, beijing_subway_belong_to_line, beijing_subway_link_src = load_data()
    beijing_subway_link = defaultdict(list)
    beijing_subway_link.update(beijing_subway_link_src)
    beijing_subway_graph = nx.Graph(beijing_subway_link)
    nx.draw(beijing_subway_graph, beijing_subway_geo_dict, with_labels=False, node_size=10)
    plt.show()


def main():
    plt_beijing_subway_line()



if __name__ == "__main__":
    main()
