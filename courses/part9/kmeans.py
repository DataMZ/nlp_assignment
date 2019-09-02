#! /usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans
import random
import matplotlib.pyplot as plt
from collections import defaultdict

X = [random.randint(0, 100) for _ in range(100)]
Y = [random.randint(0, 100) for _ in range(100)]

plt.scatter(X, Y)
tranning_data = [[x, y] for x, y in zip(X, Y)]
plt.show()

cluster = KMeans(n_clusters=6, max_iter=500)

cluster.fit(tranning_data)

print(cluster.cluster_centers_)  # 聚类中心点
print(cluster.labels_)  # 聚类标签

centers = defaultdict(list)

for label, location in zip(cluster.labels_,tranning_data):
    centers[label].append(location)

color = ['red', 'green', 'grey', 'black', 'yellow', 'orange']

for i,c in enumerate(centers):
    for location in centers[c]:
        plt.scatter(*location, c=color[i])

for center in cluster.cluster_centers_:
    plt.scatter(*center, s=100)

plt.show()
