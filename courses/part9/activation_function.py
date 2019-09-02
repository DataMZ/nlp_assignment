#! /usr/bin/python
# -*- coding: utf-8 -*-
import random

import matplotlib.pyplot as plt
import random
import numpy as np
from functools import reduce


def relu(x):
    return x if x > 0 else 0


def linear():
    w, b = random.randint(-100, 100), random.randint(-100, 100)

    def _linear(x):
        return w * x + b

    return _linear


def sigmoid(x):
    return 1 / (1 + np.e ** (-x))


def add_1(x): return x + 1


def add_2(x): return x + 2


X = np.linspace(-1000, 1000, 4000)

# 三种线性函数
L = linear()
L2 = linear()
L3 = linear()

initial = 0


def chain(funcs, x):
    last_value = funcs[0](x)
    if len(funcs) == 1:
        return last_value
    else:
        return chain(funcs[1:], last_value)


print(chain([add_1, add_2, add_2, add_1], 0))


def tanh(x):
    return np.tanh(x)

computing_chain = [linear(),relu,linear(),relu,linear(),relu]

Y = [chain(computing_chain,x) for x in X]

plt.plot(X,Y)
plt.show()


