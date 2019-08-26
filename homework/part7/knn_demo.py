#! /usr/bin/python
# -*- coding: utf-8 -*-
import math
from functools import lru_cache

from numba import njit
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle
from gensim import corpora
from gensim import models
from scipy.spatial.distance import cosine
from collections import Counter
import numpy as np
import time

"""
 knn 这种方式如果数据量很大的情况下，会导致数据计算复杂度增大
"""


def load_data():
    return pd.read_csv("D:/nlp/corpus/sqlResult_1558435_clean/train.csv"), \
           pd.read_csv("D:/nlp/corpus/sqlResult_1558435_clean/validation.csv"), \
           pd.read_csv("D:/nlp/corpus/sqlResult_1558435_clean/test.csv")


def train_model_by_sklearn():
    """
    这种训练方式的弊端是只能保存模型、idf值、词库，无法通过给定的新语料，计算
    :return:
    """
    raw_data, validation_data, test_data = load_data()
    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(raw_data["content"])
    # pickle.dump(vectorizer, open("D:/nlp/model/knn/news_knn.pickle", "wb"))
    # vectorizer.get_feature_names() # 获取所有词典里的词
    # vectorizer.vocabulary_["此外"] # 获取所有词对应的索引
    # vectorizer.idf_ # 词典对应的idf值


def load_model_by_sklearn():
    """
    导入pickle模型对象,用pickle导入导出的问题是后面不能出现方法名称
    :return:
    """
    return pickle.load(open("D:/nlp/model/knn/news_knn.pickle", "rb"))


def train_model_by_gensim():
    """
    用gensim训练模型，并保存新闻的knn的模型以及knn字典
    :return: null
    """
    raw_data, validation_data, test_data = load_data()
    words_list = [str(item).split(" ") for item in raw_data["content"]]
    dictionary = corpora.Dictionary(words_list)
    new_corpus = [dictionary.doc2bow(text) for text in words_list]
    tfidf = models.TfidfModel(new_corpus)
    tfidf.save("D:/nlp/model/knn/news_knn.tfidf")
    pickle.dump(dictionary, open("D:/nlp/model/knn/news_knn_dictionary.pickle", "wb"))


def load_model_by_gensim():
    """
    用gensim导入模型和字典库
    :return:
    """
    return models.TfidfModel.load("D:/nlp/model/knn/news_knn.tfidf"), \
           pickle.load(open("D:/nlp/model/knn/news_knn_dictionary.pickle", "rb"))


def knn_model(X, y):
    return [(Xi, yi) for Xi, yi in zip(X, y)]


def cos_distance(x1, x2):
    x1_abs = np.sqrt(np.sum(np.square(x1.values),axis=0))
    x2_abs = np.sqrt(np.sum(np.square(x2.values),axis=0))
    x1_x2_interset = set(x1.keys) & set(x2.keys)
    x1_x2_dot = np.sum([x1[item]*x2[item] for item in x1_x2_interset])
    return x1_x2_dot/(x1_abs * x2_abs)


def knn_predict(x, X, y, k=10):
    top_k_list = []
    max_top_k_distance = 10000000000000
    for x_, y_ in knn_model(X, y):
        distance = cos_distance(x, x_)
        if len(top_k_list) != 0:
            max_top_k_distance = max(item[1] for item in top_k_list)
        if len(top_k_list) < k:
            top_k_list.append((y_, distance))
        elif max_top_k_distance > distance:
            top_k_list = [(y_, distance) if item[1] == max_top_k_distance else item for item in top_k_list]
    most_similar_y = Counter([item[0] for item in top_k_list]).most_common(1)[0][0]
    return most_similar_y


# @njit
# def dict2numpy(dict, length):
#     array_ = np.zeros(length)
#     for key, value in dict:
#         array_[key] = value
#     return array_


def main():
    # train_model_by_gensim()
    start = time.time()
    raw_data, validation_data, _ = load_data()
    model, dictionary = load_model_by_gensim()
    train_y_all = list(raw_data["is_xinhua"])
    train_x_all = []
    for train_x in raw_data["content"]:
        string_list = str(train_x).split(" ")
        string_bow = dictionary.doc2bow(string_list)
        train_x_all.append(model[string_bow])
    for validation_x in validation_data["content"]:
        string_list = str(validation_x).split(" ")
        string_bow = dictionary.doc2bow(string_list)
        print(knn_predict(string_bow, train_x_all, train_y_all))
        break
    end = time.time()
    seconds = end - start
    m,s = divmod(seconds,60)
    h,m = divmod(m,60)
    # for validation
    print("%02d:%02d:%02d" % (h, m, s))


if __name__ == '__main__':
    main()
