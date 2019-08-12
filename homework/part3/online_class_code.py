#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
from functools import wraps, lru_cache
from collections import defaultdict
import time

os.chdir("D:/work_files/pycharm_codes/nlp_assignment")


def memo(f):
    """
    动态规划，用于存储中间结果，用于优化代码
    :param f: function 函数
    :return: 一个装饰器
    """
    already_computed = {}

    @wraps(f)
    def _warp(arg):
        result = None

        if arg in already_computed:
            result = already_computed[arg]
        else:
            result = f(arg)
            already_computed[arg] = result
        return result

    return _warp


def get_call_time(func):
    @wraps(func)
    def _inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("function called time is : {}".format(time.time() - start))
        return result

    return _inner


@get_call_time
def func_1(n):
    """
    @param n: is the number of customers
    @return int: the customers value point
    """
    for i in range(n):
        print(n)
    return 0


solution = {}


# 编辑距离
@lru_cache(maxsize=2 ** 10)
def edit_distance(string1, string2):
    if len(string1) == 0: return len(string2)
    if len(string2) == 0: return len(string1)

    tail_s1 = string1[-1]
    tail_s2 = string2[-1]

    candidates = [
        (edit_distance(string1[:-1], string2) + 1, "DEL {}".format(tail_s1)),  # string1 delete tail
        (edit_distance(string1, string2[:-1]) + 1, "ADD {}".format(tail_s2))
    ]

    if tail_s1 == tail_s2:
        both_forward = (edit_distance(string1[:-1], string2[:-1]) + 0, "")
    else:
        both_forward = (edit_distance(string1[:-1], string2[:-1]) + 1, 'SUB {} => {}'.format(tail_s1, tail_s2))

    candidates.append(both_forward)

    min_distance, operation = min(candidates, key=lambda x: x[0])

    solution[(string1, string2)] = operation

    return min_distance


def main():
    # original_price = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    # price = defaultdict(int)
    # for i, p in enumerate(original_price):
    #     price[i + 1] = p

    print(edit_distance('ABCDE', 'ABCCEF'))
    print(solution)


if __name__ == '__main__':
    main()
