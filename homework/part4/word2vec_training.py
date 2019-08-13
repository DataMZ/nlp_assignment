#! /usr/bin/python
# -*- coding: utf-8 -*-
from gensim.models import word2vec
from gensim.models.word2vec import LineSentence
from gensim.test.utils import datapath


def main():
    sentences = LineSentence(datapath('lee_background.cor'))
    model = word2vec.Word2Vec(sentences, size=256, window=5, min_count=5, workers=3)
    model.save("D:/nlp/model/word2vec/word2vec.model")


if __name__ == '__main__':
    main()
