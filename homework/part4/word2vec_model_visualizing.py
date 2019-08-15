#! /usr/bin/python
# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []
    for word in model.most_similar("活动",topn=25):
        tokens.append(model.wv[word[0]])
        labels.append(word[0])
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
    print(len(x))
    print(len(y))

    plt.figure(figsize=(10, 10))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom',
                     fontsize=14)
    plt.show()


def main():
    model = Word2Vec.load("D:/nlp/model/word2vec/word2vec.model")
    tsne_plot(model)
    # plt.scatter([1,2],[3,4])
    # plt.show()


if __name__ == '__main__':
    main()
