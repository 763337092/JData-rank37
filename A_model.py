# -*- coding:UTF-8 -*-
import csv
import xgboost as xgb
import numpy as np
import pandas as pd
import os

import A_valid_and_pred
import A_fetch_feature
import A_split_data

def xgb_model(train_data, train_label, test_data, test_label):
    clf = xgb.XGBClassifier(max_depth=7,
                           min_child_weight=1,
                           learning_rate=0.1,
                           n_estimators=500,
                           silent=True,
                           objective='binary:logistic',
                           gamma=0,
                           max_delta_step=0,
                           subsample=1,
                           colsample_bytree=1,
                           colsample_bylevel=1,
                           reg_alpha=0,
                           reg_lambda=0,
                           scale_pos_weight=1,
                           seed=1,
                           missing=None)
    clf.fit(train_data, train_label, eval_metric='auc', verbose=True,
            eval_set=[(test_data, test_label)], early_stopping_rounds=100)
    y_pre = clf.predict(test_data)
    y_pro = clf.predict_proba(test_data)[:, 1]
    #print "AUC Score : %f" % metrics.roc_auc_score(test_label, y_pro)
    #print"Accuracy : %.4g" % metrics.accuracy_score(test_label, y_pre)
    return clf

if __name__ == '__main__':
    print 'Train model!'
    '''###################切分数据#########################'''
    #A_split_data.split_data() #把历史数据按天进行切分，便于后续使用
    '''###################生成验证集#########################'''
    A_valid_and_pred.make_validate_file()
    if not os.path.exists('pred'):
        os.mkdir('pred')
    ###################################PRED ONLINE##############################################
    #"""
    '''###############################采用时间滑动窗口构建数据集##################################'''
    A_fetch_feature.get_data_by_slide_windows(start_day=61, windows=10, pos_file='data/pos_pred.csv', neg_file='data/neg_pred.csv')
    length_pos = len(pd.read_csv('data/pos_pred.csv'))
    '''###############################MODEL1##################################'''
    '''############用五套数据，训练5个xgboost模型，分别进行预测，保存5个预测文件#############'''
    for i in range(5):
        '''负样本下采样，保证正负样本比例为1：11'''
        A_fetch_feature.down_sample_neg_data(input_file='data/neg_pred.csv',
                                             output_file='data/neg_pred_down%s.csv' % str(i), length_pos=length_pos, rate=11)
        '''训练测试集获取'''
        train_data, train_label, test_data, test_label = \
            A_fetch_feature.get_data(pos_file='data/pos_pred.csv', neg_file='data/neg_pred_down%s.csv' % str(i))
        '''xgboost模型训练'''
        GBRT = xgb_model(train_data, train_label, test_data, test_label)
        '''生成一个预测文件，有顺序地保留前5000个用户对到文件中'''
        A_valid_and_pred.predict_new2(model=GBRT, file_name='pred/pred5_22_1_%s.csv' % str(i), start_day=75, state='test',
                                      choose_num=5000)
    vote_dict = dict()
    '''####################对5个模型生成的结果进行投票，得到最终预测结果###################'''
    for i in range(5):
        r_file = file('pred/pred5_22_1_%s.csv' % str(i), 'r')
        reader = csv.reader(r_file)
        index = 5000
        for line in reader:
            if reader.line_num == 1:
                continue
            if (line[0], line[1]) not in vote_dict:
                vote_dict[(line[0], line[1])] = 0
            vote_dict[(line[0], line[1])] += index
            index -= 1
    sort_vote = sorted(vote_dict.iteritems(), key=lambda d: d[1], reverse=True)
    w_file = file('pred/f5000.csv', 'w')
    writer = csv.writer(w_file)
    writer.writerow(['user_id', 'sku_id'])
    unique_score_key = {}
    index = 0
    choose_unique = dict()
    for item in sort_vote:
        if item[0][0] not in choose_unique:
            choose_unique[item[0][0]] = item[0][1]
            writer.writerow(item[0])
            index += 1
            if index > 5000:
                break
    print index
    w_file.close()#
    # """
    '''###################生成预测文件#########################'''
    A_valid_and_pred.make_submission_file()
    #"""

###################################VALLID OFLINE##############################################
    """
    #A_fetch_feature.get_data_by_slide_windows(start_day=56, windows=10, pos_file='data/pos5_18_.csv', neg_file='data/neg5_18_.csv')
    length_pos = len(pd.read_csv('data/pos5_18_.csv'))
    '''###########################MODEL1#############################################'''
    for i in range(5):
        #A_fetch_feature.down_sample_neg_data(input_file='data/neg5_18_.csv', output_file='data/neg5_18_down%s.csv' %str(i), length_pos=length_pos, rate=11)
        train_data, train_label, test_data, test_label = \
            A_fetch_feature.get_data(pos_file='data/pos5_18_.csv', neg_file='data/neg5_18_down%s.csv' %str(i))

        GBRT = xgb_model(train_data, train_label, test_data, test_label)

        A_valid_and_pred.predict_new2(model=GBRT, file_name='test/pred04_11_15_%s.csv' %str(i), start_day=70,
                                      state='test', choose_num=1136)
        A_valid_and_pred.score_valid(pred_file='test/pred04_11_15_%s.csv' %str(i), test_file='test/buy_04_11_15.csv')

    print "**********start voting*************"
    vote_dict = dict()
    for i in range(5):
        r_file = file('test/pred04_11_15_%s.csv' %str(i), 'r')
        reader = csv.reader(r_file)
        index = 1137
        for line in reader:
            if reader.line_num == 1:
                continue
            if (line[0], line[1]) not in vote_dict:
                vote_dict[(line[0], line[1])] = 0
            vote_dict[(line[0], line[1])] += index
            index -= 1
    sort_vote = sorted(vote_dict.iteritems(), key=lambda d: d[1], reverse=True)
    for i in range(1140, 600, -10):
        w_file = file('test/pred04_11_15.csv', 'w')
        writer = csv.writer(w_file)
        writer.writerow(['user_id', 'sku_id'])
        unique_score_key = {}
        index = 0
        for item in sort_vote:
            #print item
            writer.writerow(item[0])
            index += 1
            if index > i:
                break
        print index
        w_file.close()

        #for i in range(400, 1101, 100):
        A_valid_and_pred.score_valid(pred_file='test/pred04_11_15.csv', test_file='test/buy_04_11_15.csv')
    print "**********end voting*************"

    """