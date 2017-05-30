# -*- coding:UTF-8 -*-
import os
import csv
import numpy as np
import pandas as pd
import A_fetch_feature
import A_info_dict

def validatef11(pred_file, test_file):
    pred = np.loadtxt(open(pred_file, 'r'), delimiter=",", skiprows=1, dtype=int)
    # pred = unique(pred)
    test = np.loadtxt(open(test_file, 'r'), delimiter=",", skiprows=0, dtype=int)

    len_pred = len(pred)
    len_test = len(test)
    correct_num = 0
    for index_pred in range(len_pred):
        for index_test in range(len_test):
            if pred[index_pred, 0] == test[index_test, 0]:
                correct_num += 1

    precise = float(correct_num) / float(len_pred)
    recall = float(correct_num) / float(len_test)

    if (5*recall+precise) == 0:
        return 0
    else:
        return 6*recall*precise/(5*recall+precise)


def validatef12(pred_file, test_file):
    pred = np.loadtxt(open(pred_file, 'r'), delimiter=",", skiprows=1, dtype=int)
    # pred = unique(pred)
    test = np.loadtxt(open(test_file, 'r'), delimiter=",", skiprows=0, dtype=int)

    len_pred = len(pred)
    len_test = len(test)
    correct_num = 0
    for index_pred in range(len_pred):
        for index_test in range(len_test):
            if (pred[index_pred, 0] == test[index_test, 0]) and (pred[index_pred, 1] == test[index_test, 1]):
                correct_num += 1

    precise = float(correct_num) / float(len_pred)
    recall = float(correct_num) / float(len_test)

    if (2*recall+3*precise) == 0:
        return 0
    else:
        return 5*recall*precise/(2*recall+3*precise)


"""
对预测结果打分
    pred_file：预测文件（不含表头）
    test_file：正确答案文件
"""
def score_valid(pred_file, test_file):
    pred = np.loadtxt(open(pred_file, 'r'), delimiter=",", skiprows=1, dtype=int)
    test = np.loadtxt(open(test_file, 'r'), delimiter=",", skiprows=0, dtype=int)
    len_pred = len(pred)
    len_test = len(test)
    correct_num1 = 0
    correct_num2 = 0
    for index_pred in range(len_pred):
        for index_test in range(len_test):
            if pred[index_pred, 0] == test[index_test, 0]:
                correct_num1 += 1
            if (pred[index_pred, 0] == test[index_test, 0]) and (pred[index_pred, 1] == test[index_test, 1]):
                correct_num2 += 1
    precise1 = float(correct_num1) / float(len_pred)
    recall1 = float(correct_num1) / float(len_test)
    if (2*recall1+3*precise1) == 0:
        f11 = 0
    else:
        f11 = 6 * recall1 * precise1 / (5 * recall1 + precise1)

    precise2 = float(correct_num2) / float(len_pred)
    recall2 = float(correct_num2) / float(len_test)
    if (2 * recall2 + 3 * precise2) == 0:
        f12 = 0
    else:
        f12 = 5 * recall2 * precise2 / (2 * recall2 + 3 * precise2)

    score = 0.4*f11 + 0.6*f12
    print score, "(F11:", f11,"/F12:", f12,")"
    return score, f11, f12

def predict_new2(model, file_name, start_day=1, state='test', choose_num = 1130):
    ten_day_action = A_fetch_feature.get_feature(start_day, state)
    test_label_list = []
    for key in ten_day_action:
        test_label_list.append(ten_day_action[key])
    pred = model.predict_proba(np.array(test_label_list))[:, 1]
    #print pred
    index = 0
    score_dict = {}
    for key in ten_day_action:
        if key[0] not in score_dict:
            score_dict[key[0]] = [key[1], pred[index]]
        else:
            if score_dict[key[0]][1] < pred[index]:
                score_dict[key[0]] = [key[1], pred[index]]
        index += 1
    pred_dict = {}
    for key in score_dict:
        pred_dict[(key, score_dict[key][0])] = score_dict[key][1]
    sort_pred = sorted(pred_dict.iteritems(), key=lambda d: d[1], reverse=True)

    w_file = file(file_name, 'w')
    writer = csv.writer(w_file)
    writer.writerow(['user_id', 'sku_id'])
    unique_score_key = {}
    index = 0
    for item in sort_pred:
        #print item
        writer.writerow(item[0])
        index += 1
        if index > choose_num:
            break
    #print index
    w_file.close()

def make_validate_file():
    UI_buy_set = set()
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('test'):
        os.mkdir('test')
    for i in range(71, 76):
        file_name = 'Day/%s.csv' % (str(i))
        r_file = file(file_name, 'r')
        reader = csv.reader(r_file)
        for line in reader:
            if line[2] == '4':
                UI_buy_set.add((line[0], line[1]))
        r_file.close()
    w_file = file('test/buy_04_11_15.csv', 'w')
    writer = csv.writer(w_file)
    writer.writerow(['user_id', 'sku_id'])
    for item in UI_buy_set:
        writer.writerow(item)
    w_file.close()

def make_submission_file():
    #ui_dict = A_info_dict.high_rate_usr_dict()

    five_thousand_dict = dict()
    five_thousand_lst = pd.read_csv('pred/f5000.csv').values
    '''
    for line in five_thousand_lst:
        five_thousand_dict[line[0]] = line[1]
    same_dict = dict()
    for item in ui_dict:
        if item in five_thousand_dict:
            ui_dict[item] = five_thousand_dict[item]
            same_dict[item] = five_thousand_dict[item]
    index = 0
    for item in five_thousand_dict:
        if item not in ui_dict:
            same_dict[item] = five_thousand_dict[item]
            ui_dict[item] = five_thousand_dict[item]
        index += 1
        if index == 50:
            break
    ui_dict = A_info_dict.high_rate_usr_dict()
    print len(same_dict)  # 538
    print len(ui_dict)
    '''
    w_file = file('submission.csv', 'w')
    writer = csv.writer(w_file)
    writer.writerow(['user_id', 'sku_id'])
    #for key in ui_dict:
    #    writer.writerow([key, ui_dict[key]])
    index = 0
    for line in five_thousand_lst:
        writer.writerow(line)
        index += 1
        if index >=1000:
            break
    w_file.close()

if __name__ == '__main__':
    print 'Validate and predict!'
    make_validate_file()