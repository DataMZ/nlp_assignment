#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
from collections.abc import Iterable
from functools import lru_cache

from geopy.geocoders import Nominatim
from urllib import parse
import hashlib
import requests
import json
import math




def get_url(address):
    # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=你的ak
    queryStr = '/geocoder/v2/?address=%s&output=json&ak=mAiGweYSlAt0pGYDOetmyOByRUEzpiSG' % address
    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    # 在最后直接追加上yoursk
    rawStr = encodedStr + 'Rx2n282wzMACr4Iu1tNvPxmWFjC9VTOL'
    # 计算sn
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
    # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
    return url


def flatten(x):
    result = []
    for el in x:
        if isinstance(x, Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

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


if __name__ == "__main__":
    import matplotlib

    print(matplotlib.__path__)

    # a= {1:2,2:3}
    # print(list(zip(a.keys(),a.values())) )
    # print(list(a))
    # print(a)

    dic = {0: (-41, -81), 1: (-39, -71), 2: (-2, 87)}
    print(geo_distance(dic[0],dic[1]))
    print(geo_distance(dic[1],dic[2]))
    print(geo_distance(dic[0],dic[1]) + geo_distance(dic[1],dic[2]))
    print(geo_distance(dic[0],dic[2]) + geo_distance(dic[2],dic[1]))
