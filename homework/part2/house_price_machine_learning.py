#! /usr/bin/python
# -*- coding: utf-8 -*-
import matplotlib
from sklearn.datasets import load_boston
import matplotlib.pyplot as plt
import random


def price(rm,k,b):
    return k * rm + b

def loss(y,y_hat):
    return sum((y_i - y_hat_i) ** 2 for y_i,y_hat_i in zip(list(y),list(y_hat))) / len(list(y))

def draw_rm_and_price():
    plt.scatter(X[:, 5], y)


def partial_k(x, y, y_hat):
    n = len(y)

    gradient = 0

    for x_i, y_i, y_hat_i in zip(list(x), list(y), list(y_hat)):
        gradient += (y_i - y_hat_i) * x_i

    return -2 / n * gradient


def partial_b(y, y_hat):
    n = len(y)

    gradient = 0

    for y_i, y_hat_i in zip(list(y), list(y_hat)):
        gradient += (y_i - y_hat_i)

    return -2 / n * gradient

if __name__ == "__main__":

    data = load_boston()
    X,y = data["data"],data["target"]

    X_rm = X[:,5]
    # k = random.randint(-100,100)
    # b = random.randint(-100,100)
    # print(k)
    # print(b)
    # price_by_random_k_and_b = [price(r,k,b) for r in X_rm]
    # plt.scatter(X_rm, price_by_random_k_and_b)
    # plt.show()



    # First-Method:Random generation: get best k and best b
    # trying_times = 2000
    #
    # min_loss = float('inf')
    # best_k, best_b = None, None
    #
    # for i in range(trying_times):
    #     k = random.random() * 200 - 100
    #     b = random.random() * 200 - 100
    #     price_by_random_k_and_b = [price(r, k, b) for r in X_rm]
    #
    #     current_loss = loss(y, price_by_random_k_and_b)
    #
    #     if current_loss < min_loss:
    #         min_loss = current_loss
    #         best_k, best_b = k, b
    #         print(
    #             'When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, best_k, best_b, min_loss))

    # Second-Method: Direction Adjusting
    # trying_times = 2000
    #
    # min_loss = float('inf')
    #
    # best_k = random.random() * 200 - 100
    # best_b = random.random() * 200 - 100
    #
    # direction = [
    #     (+1, -1),  # first element: k's change direction, second element: b's change direction
    #     (+1, +1),
    #     (-1, -1),
    #     (-1, +1),
    # ]
    #
    # next_direction = random.choice(direction)
    #
    # scalar = 0.1
    #
    # update_time = 0
    #
    # for i in range(trying_times):
    #
    #     k_direction, b_direction = next_direction
    #
    #     current_k, current_b = best_k + k_direction * scalar, best_b + b_direction * scalar
    #
    #     price_by_k_and_b = [price(r, current_k, current_b) for r in X_rm]
    #
    #     current_loss = loss(y, price_by_k_and_b)
    #
    #     if current_loss < min_loss: # performance became better
    #         min_loss = current_loss
    #         best_k, best_b = current_k, current_b
    #
    #         next_direction = next_direction
    #         update_time += 1
    #
    #         if update_time % 10 == 0:
    #             print('When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, best_k, best_b, min_loss))
    #     else:
    #         next_direction = random.choice(direction)

    # Third：Gradient Descent to get optimal k and b
    trying_times = 2000

    min_loss = float('inf')

    current_k = random.random() * 200 - 100
    current_b = random.random() * 200 - 100

    learning_rate = 1e-04

    update_time = 0

    for i in range(trying_times):
        price_by_k_and_b = [price(r, current_k, current_b) for r in X_rm]
        current_loss = loss(y, price_by_k_and_b)

        if current_loss < min_loss:  # performance became better
            min_loss = current_loss
            if i % 50 == 0:
                print('When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, current_k, current_b,
                                                                                                 min_loss))
        k_gradient = partial_k(X_rm, y, price_by_k_and_b)
        b_gradient = partial_b(y, price_by_k_and_b)

        current_k = current_k + (-1 * k_gradient) * learning_rate
        current_b = current_b + (-1 * b_gradient) * learning_rate


