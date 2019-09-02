#! /usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from collections import Counter


def entropy(elements):
    counter = Counter(elements)
    probs = [counter[c] / len(elements) for c in elements]
    return - sum(p * np.log(p) for p in probs)


if __name__ == '__main__':
    print(entropy([1, 2, 3, 4]))
