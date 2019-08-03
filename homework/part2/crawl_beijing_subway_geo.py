#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
from collections.abc import Iterable
import requests
from urllib import parse
import hashlib

os.chdir("D:/work_files/pycharm_codes/nlp_assignment")


def flatten(x):
    result = []
    for el in x:
        if isinstance(x, Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


def get_url_by_baidu(address):
    # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=你的ak
    queryStr = '/geocoder/v2/?address=%s&region=北京&tag=地铁站&city_limit=true&output=json&ak=*' % address
    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    # 在最后直接追加上yoursk
    rawStr = encodedStr + '*'
    # 计算sn
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
    # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
    return url


def get_url_by_gaode(address):
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {"key": "*",
              "address": address,
              "city": "北京"}
    return url, params


def get_location_by_baidu(address):
    url = get_url_by_baidu(address)
    response = requests.get(url).json()
    if response["status"] == 0:
        longitude = response["result"]["location"]["lng"]
        latitude = response["result"]["location"]["lat"]
        return longitude, latitude
    else:
        return "", ""


def get_location_by_gaode(address):
    url, params = get_url_by_gaode(address)
    response = requests.get(url, params).json()
    print(response)
    if response["status"] == "1" and len(response["geocodes"]) != 0:
        for item in response['geocodes']:
            location = item["location"].split(",")
            longitude = location[0]
            latitude = location[1]
            return longitude, latitude
    else:
        return "", ""


def get_beijing_subway_geo():
    all_subway_station = []
    with open("homework/part2/data/beijing_subway_line.txt", "r", encoding="utf-8") as beijing_subway_line_file:
        for line in beijing_subway_line_file.readlines():
            all_subway_station.append(line.strip().split(":")[1].split(","))
    all_unique_subway_station = list(set(flatten(all_subway_station)))

    for site in all_unique_subway_station:
        # longitude, latitude = get_location_by_baidu("{}".format(site))
        longitude, latitude = get_location_by_gaode("{}地铁站".format(site))
        print("{}:{},{}".format(site, longitude, latitude))


def main():
    get_beijing_subway_geo()
    # print(get_location_by_gaode("四道桥站地铁站"))


if __name__ == '__main__':
    main()
