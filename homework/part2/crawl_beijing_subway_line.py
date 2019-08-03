#! /usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import *
import re
import os

os.chdir("D:/work_files/pycharm_codes/nlp_assignment")


def get_request_soup(url):
    """
    根据URL请求并返回soup类型
    :param url: string 正式的url
    :return: soup,请求返回的soup
    """
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }  # 请求头
    html_request = requests.get(url, headers=headers, allow_redirects=False)
    html_request.encoding = 'utf-8'
    return BeautifulSoup(html_request.text, 'lxml')


def get_url_list():
    """
    根据特定的父网址,添加子网址
    :return: 返回所有网址链接
    """
    main_url_soup = get_request_soup("https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485")
    sub_url_list = ["https://baike.baidu.com{}".format(item.get("href")) for item in
                    main_url_soup.find_all("table")[2].find_all("a")][:-1]
    return sub_url_list


def get_beijing_subway_line():
    sub_url_list = get_url_list()
    beijing_subway_line = []
    for sub_url in set(sub_url_list):
        sub_url_soup = get_request_soup(sub_url)
        title = str(sub_url_soup.title.text).replace("_百度百科", "")
        result_list = []
        for item in sub_url_soup.find_all("table"):
            if re.findall(u"时刻表|时间表|首车时间|往燕山|YZ01", item.text):  # 时刻表|时间表|首车时间 共性 往燕山-燕房线 YZ01-亦庄线
                tmp_result = [str(sub_item.find("th").text).strip() if sub_item.find("th") is not None else "" for
                              sub_item in item.find_all("tr")]
                empty_probability = sum([1 if item == "" else 0 for item in tmp_result]) / len(tmp_result)
                if empty_probability > 0.5 or title.__contains__("亦庄线"):
                    tmp_result = [str(sub_item.find("td").text).strip() if sub_item.find("td") is not None else "" for
                                  sub_item in item.find_all("tr")]
                result_list.append(
                    [sub_item for sub_item in tmp_result if
                     (not ["", "车站名称", "全程", "首车时间", "北京地铁1号线首末车时刻表", "时间", "备注"].__contains__(sub_item))
                     and (not re.findall(u"\n|【|】", sub_item))])
        if len(result_list) == 1:
            beijing_subway_line.append((title, result_list[0]))
        elif len(result_list) > 1:
            for index, line in enumerate(result_list):
                beijing_subway_line.append(("{}-{}".format(title, index), line))
    return beijing_subway_line


def main():
    with open("homework/part2/data/beijing_subway_line.txt", "w",encoding="utf-8") as beijing_subway_line_file:
        beijing_subway_line = get_beijing_subway_line()
        for title, line in beijing_subway_line:
            beijing_subway_line_file.write("{}:{}\n".format(title, ",".join(line)))


if __name__ == "__main__":
    main()
