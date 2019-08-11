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
    """
    绘制北京地铁路线图
    :return: 无返回值
    """
    beijing_subway_geo_dict, beijing_subway_line, beijing_subway_belong_to_line, beijing_subway_link_src = load_data()
    beijing_subway_link = defaultdict(list)
    beijing_subway_link.update(beijing_subway_link_src)
    beijing_subway_graph = nx.Graph(beijing_subway_link)
    nx.draw(beijing_subway_graph, beijing_subway_geo_dict, with_labels=False, node_size=10)
    plt.show()


def first_search(graph, start, rule="depth_first"):
    """
    用深度优先或者广度优先的搜索策略搜索整个图
    :param graph: dict,图结构，形如 {"北京":["太原","沈阳"],...}
    :param start: string,开始地名
    :param rule: string,规则,比如depth_first,breath_first
    :return: 遍历后的元素
    """
    visited = [start]
    seen = set()
    while visited:
        froninter = visited.pop()  # 删除列表中最后一个值,并返回最后一个值
        if froninter in seen: continue
        for successor in graph[froninter]:
            if successor in seen: continue
            print(successor)
            if rule == "depth_first":
                visited = visited + [successor]  # 我们每次扩展都扩展最新发现的点 -> depth first
            else:
                visited = [successor] + visited  # 我们每次扩展都先考虑已经发现的 老的点 -> breath first
            # 所以说，这个扩展顺序其实是决定了我们的深度优先还是广度优先
        seen.add(froninter)
    return seen


def search(start, destination, connection_graph, sort_candidate):
    """
    给定初始位置和结束位置，以及图结构和排序规则，利用排序规则获取最优分布路径。
    :param start: string,开始位置
    :param destination: string,结束位置
    :param connection_graph: dict,图结构,形如{"a":["b","c"]}
    :param sort_candidate: 排序函数
    :return: path, [], 最优路径
    """
    pathes = [[start]]

    visited = set()

    while pathes:
        path = pathes.pop(0)
        froninter = path[-1]

        if froninter in visited: continue

        successors = connection_graph[froninter]

        for node in successors:
            if node in path: continue
            new_path = path + [node]
            pathes.append(new_path)
            if node == destination: return new_path
        visited.add(froninter)
        pathes = sort_candidate(pathes)  # 我们可以加一个排序函数 对我们的搜索策略进行控制


def transfer_station_first(pathes):
    """
    经过站数最少
    :param pathes: [] 路径列表,[path1,path2]
    :return: function
    """
    return sorted(pathes, key=len)  # 升序


def transfer_as_much_possible(pathes):
    """
    经过站数最多
    :param pathes:  [] 路径列表,[path1,path2]
    :return: function
    """
    return sorted(pathes, key=len, reverse=True)


def get_path_distance(path):
    """
    获取路径距离
    :param path:[] 整个路径
    :return: 距离和
    """
    distance = 0.0
    for i in range(len(path) - 1):
        distance += geo_distance(path[i], path[i + 1])
    return distance


def shortest_path_first(pathes):
    """
    最短路径距离
    :param pathes:  [] 路径列表,[path1,path2]
    :return: function
    """
    if len(pathes) <= 1: return pathes
    return sorted(pathes, key=get_path_distance)


def main():
    plt_beijing_subway_line()


if __name__ == "__main__":
    main()
