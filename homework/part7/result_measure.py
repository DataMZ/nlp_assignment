#! /usr/bin/python
# -*- coding: utf-8 -*-
import os

os.chdir("D:/work_files/pycharm_codes/nlp_assignment")


def cal_measure_index():
    with open("homework/part7/result/result_file.txt", "r") as result_file:
        tp = 0
        fp = 0
        fn = 0
        tn = 0
        for line in result_file.readlines():
            line_result = [int(item) for item in line.split(",")]
            if line_result[0] == 1 and line_result[1] == 1:
                tp += 1
            elif line_result[0] == 0 and line_result[1] == 1:
                fp += 1
            elif line_result[0] == 1 and line_result[1] == 0:
                fn += 1
            else:
                tn += 1
        accuracy = float(tp + tn) / float(tp + fp + fn + tn)
        precision = float(tp) / float(tp + fp)
        recall = float(tp) / float(tp + fn)
        f = 2 / (1 / precision + 1 / recall)
        return accuracy, precision, recall, f


def main():
    print(cal_measure_index())


if __name__ == '__main__':
    main()
