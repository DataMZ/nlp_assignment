#! /usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import os
import jieba
import re
from collections import Counter

os.chdir("D:/work_files/pycharm_codes/nlp_assignment")


def token(string):
    return re.findall("\w+", string)


def cut(string):
    return list(jieba.cut(string))


def prob_1(word, words_count, token): return words_count[word] / len(token)


def prob_2(word1, word2, words_count, token):
    if "%s%s".format(word1, word2) in words_count:
        return words_count["%s%s".format(word1, word2)] / len(token)
    else:
        return 1 / len(token)


def prob_3(word1, word2, word3, words_count, token):
    if "%s%s%s".format(word1, word2, word3) in words_count:
        return words_count["%s%s%s".format(word1, word2, word3)] / len(token)
    else:
        return 1 / len(token)


def get_probablity_3(sentence, words_count, token):
    words = cut(sentence)

    sentence_pro = 1

    for i, word in enumerate(words[:-2]):
        next_1 = words[i + 1]
        next_2 = words[i + 2]

        probability = prob_3(word, next_1, next_2, words_count, token)

        sentence_pro *= probability

    return sentence_pro


if __name__ == "__main__":
    # 提取关键字符(非标点符号)
    # content = pd.read_csv("homework/part1/data/movie_comments.csv")
    # contents = content["comment"].tolist()
    # contents_clean = ["".join(token(str(c))) for c in contents]
    # with open("homework/part1/result/content_clean.txt","w",encoding="utf-8") as f:
    #     for c in contents_clean:
    #         f.write(c + "\n")
    # 分词计算生成2-gram模型
    TOKEN = []
    for i, line in enumerate(open("homework/part1/result/content_clean.txt", "r", encoding="utf-8")):
        if i % 100 == 0: print(i)
        if i > 100000: break
        TOKEN += cut(line)

    TOKEN_3_GRAM = [''.join(TOKEN[i:i + 3]) for i in range(len(TOKEN[:-3]))]
    words_count_3 = Counter(TOKEN_3_GRAM)
    print(get_probablity_3("真事一只好看的小猫", words_count_3, TOKEN_3_GRAM))
    print(get_probablity_3("真是一只好看的小猫", words_count_3, TOKEN_3_GRAM))
