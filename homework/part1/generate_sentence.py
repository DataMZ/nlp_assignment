#! /usr/bin/python
# -*- coding: utf-8 -*-
import random


def create_grammar(grammar_str, split="=>", line_split="\n"):
    grammar = {}
    for line in grammar_str.split(line_split):
        if not line.strip(): continue
        exp, stmt = line.split(split)
        grammar[exp.strip()] = [s.split() for s in stmt.split("|")]
    return grammar


def generate(gram, target):
    if target not in gram: return target
    expand = [generate(gram, t) for t in random.choice(gram[target])]
    return "".join([e if e != "/n" else "\n" for e in expand if e != "null"])


def generate_n(gram, target, n):
    sentence_list = []
    for i in range(n):
        sentence_list.append(generate(gram, target))
    return sentence_list


if __name__ == "__main__":
    human = """
    human = 自己 寻找 活动
    自己 = 我 | 俺 | 我们 
    寻找 = 看看 | 找找 | 想找点
    活动 = 乐子 | 玩的
    """
    # print(generate(create_grammar(human,split="=",line_split="\n"),target="human"))
    for item in generate_n(create_grammar(human, split="=", line_split="\n"), target="human", n=10):
        print(item)
