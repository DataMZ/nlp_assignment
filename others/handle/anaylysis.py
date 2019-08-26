#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt

os.chdir("D:/work_files/pycharm_codes/nlp_assignment")


def load_data():
    revenue = []
    ecpm = []
    aid = []
    with open("others/data/business.txt", "r", encoding="utf-8") as data_file:
        for line in data_file.readlines():
            line_split = line.split(",")
            revenue.append(float(line_split[0]))
            ecpm.append(float(line_split[1]))
            aid.append(float(line_split[2]))
    return revenue, ecpm, aid


def plot_aid_revenue(aid, revenue):
    plt.plot(aid, revenue)
    plt.title("收入-日均广告数")
    plt.xlabel("日均广告数")
    plt.ylabel("收入")
    plt.show()


def plot_ecpm_revenue(ecpm, revenue):
    plt.plot(ecpm, revenue)
    plt.title("收入-日均ecpm")
    plt.xlabel("日均ecpm")
    plt.ylabel("收入")
    plt.show()


def main():
    revenue, ecpm, aid = load_data()
    filter_fields = [(item1, item2) for item1, item2 in zip(revenue, aid) if 100 <= item2 < 1000]
    plot_aid_revenue([item[1] for item in filter_fields], [item[0] for item in filter_fields])
    # plot_ecpm_revenue(ecpm,revenue)


if __name__ == '__main__':
    main()
