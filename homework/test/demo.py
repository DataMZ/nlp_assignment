#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
from collections.abc import Iterable
from geopy.geocoders import Nominatim
from urllib import parse
import hashlib
import requests
import json


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

if __name__ == "__main__":
    a = {}
    a["1"] = []
    print(a.get("1").append("2"))
    print(a)



