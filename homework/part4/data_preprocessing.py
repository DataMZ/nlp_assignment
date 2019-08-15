#! /usr/bin/python
# -*- coding: utf-8 -*-
import jieba


def sentence_segment(text):
    """
      功能：将文本切割成单独的句子
      输入text：剧本内容，str,unicode
      输出res:切分完的句子列表,list,每个元素是一句话
      """
    res = [text]
    delimiters_list = [u'?', u'!', u';', u'？', u'！', u'。', u'；', u'----', u'——', u'……', u'…', u'\n', u'~~~', u"\\n"]
    delimiters_set = set(delimiters_list)
    for sep in delimiters_set:
        text, res = res, []
        for seq in text:
            temp_list = seq.split(sep)
            if len(temp_list) > 1:
                left_list = [item + sep for item in temp_list[0:-1]]
                temp_list = left_list + [temp_list[-1]]
            res += temp_list
    res = [s.strip() for s in res if len(s.strip()) > 0 and s.strip() not in delimiters_list]
    return res


def main():
    write_file = open("D:/nlp/corpus/clean/word2vec_corpus-1.txt", "w", encoding="utf-8")
    line_num = 0
    with open("D:/nlp/corpus/sohu-20130820-20161031/sohu-20130820-20161031.txt", "r", encoding="utf-8") as read_file:
        while 1:
            line = read_file.readline()
            if not line:
                break
            sentence_list = sentence_segment(line.split("`1`2")[2])
            for sentence in sentence_list:
                seg_list = jieba.cut(sentence, cut_all=False)
                write_file.write(" ".join(seg_list))
            line_num += 1
            if line_num % 10000 == 0:
                print("finish {}".format(line_num))
                write_file.flush()


if __name__ == '__main__':
    main()
