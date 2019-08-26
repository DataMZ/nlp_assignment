#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import jieba
import random


def data_preprocess():
    data_file_path = "D:/nlp/corpus/sqlResult_1558435/sqlResult_1558435.csv"
    news = pd.read_csv(data_file_path, encoding="gb18030")
    content = news["content"]
    y = news["source"].apply(lambda x: (x == "新华社") * 1)
    tag_result = pd.DataFrame([(" ".join(jieba.cut(item1, cut_all=False)), item2) for item1, item2 in zip(content, y) if
                               isinstance(item1, str)], columns=["content", "is_xinhua"])
    tag_result.to_csv("D:/nlp/corpus/sqlResult_1558435_clean/sqlResult_clean.csv", header=True, index=False)


def data_segmentation():
    raw_data = pd.read_csv("D:/nlp/corpus/sqlResult_1558435_clean/sqlResult_clean.csv")
    train_rate = 0.6
    train_list = []
    validation_rate = 0.2
    validation_list = []
    test_rate = 1 - train_rate - validation_rate
    test_list = []
    data_list = list(zip(raw_data["content"], raw_data["is_xinhua"]))
    for item in data_list:
        random_num = random.random()
        if random_num <= train_rate:
            train_list.append(item)
        elif train_rate < random_num <= train_rate + validation_rate:
            validation_list.append(item)
        elif train_rate >= test_rate:
            test_list.append(item)
    train_df = pd.DataFrame(train_list, columns=["content", "is_xinhua"])
    train_df.to_csv("D:/nlp/corpus/sqlResult_1558435_clean/train.csv", header=True, index=False)
    validation_df = pd.DataFrame(validation_list, columns=["content", "is_xinhua"])
    validation_df.to_csv("D:/nlp/corpus/sqlResult_1558435_clean/validation.csv", header=True, index=False)
    test_df = pd.DataFrame(test_list, columns=["content", "is_xinhua"])
    test_df.to_csv("D:/nlp/corpus/sqlResult_1558435_clean/test.csv", header=True, index=False)


def main():
    data_segmentation()


if __name__ == '__main__':
    main()
