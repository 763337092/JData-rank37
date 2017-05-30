# -*- coding:UTF-8 -*-
"""
从JData_User.csv,JData_Product.csv,JData_Comment.csv三个文件获取用户/商品特征字典
"""
import csv
import numpy as np
import pandas as pd


'''遍历字典num项'''
def ergodic_dict(dict, num=5):
    index = 0
    for key in dict:
        print key, dict[key]
        index += 1
        if index > num:
            break
    print 'length:', len(dict)
    print ' '

'''遍历集合num项'''
def ergodic_set(st, num=5):
    index = 0
    for key in st:
        print key
        index += 1
        if index > num:
            break
    print 'length:', len(st)
    print ' '

'''获取用户特征字典{uID：[age, sex, rank]}
age:0,1,2,3,4,5,6
sex:0,1,2,3
rank:1,2,3,4,5
'''
def usr_feature():
    r_file = file('JData/JData_User.csv', 'r')
    reader = csv.reader(r_file)
    feature_dict = {}
    for line in reader:
        if reader.line_num == 1:
            continue
        if line[4] == 'NULL':
            reg = 0
        if line[4] != 'NULL':
            reg = int(line[4].split('-')[0])-2000
        if line[1].decode('gbk').encode('utf8') == '-1':
            feature_dict[line[0]] = [line[1], line[2], line[3], reg]
        elif line[1].decode('gbk').encode('utf8') == '56岁以上':
            feature_dict[line[0]] = ['56', line[2], line[3], reg]
        elif line[1].decode('gbk').encode('utf8') == '46-55岁':
            feature_dict[line[0]] = ['46-55', line[2], line[3], reg]
        elif line[1].decode('gbk').encode('utf8') == '36-45岁':
            feature_dict[line[0]] = ['36-45', line[2], line[3], reg]
        elif line[1].decode('gbk').encode('utf8') == '26-35岁':
            feature_dict[line[0]] = ['26-35', line[2], line[3], reg]
        elif line[1].decode('gbk').encode('utf8') == '16-25岁':
            feature_dict[line[0]] = ['16-25', line[2], line[3], reg]
        else:
            feature_dict[line[0]] = ['15', line[2], line[3], reg]
    r_file.close()
    age_dict = {'-1': [1,0,0,0,0,0,0], '15': [0,1,0,0,0,0,0], '16-25': [0,0,1,0,0,0,0],
                '26-35': [0,0,0,1,0,0,0], '36-45': [0,0,0,0,1,0,0], '46-55': [0,0,0,0,0,1,0],
                '56': [0,0,0,0,0,0,1]}
    sex_dict = {'0': [1,0,0,0], '1': [0,1,0,0], '2': [0,0,1,0], 'NULL': [0,0,0,1]}
    rank_dict = {'1': [1, 0, 0, 0, 0], '2': [0, 1, 0, 0, 0], '3': [0, 0, 1, 0, 0], '4': [0, 0, 0, 1, 0], '5': [0, 0, 0, 0, 1]}
    transfer_feature = {}
    for key in feature_dict:
        #print original_feature[key]
        transfer_feature[key] = age_dict[feature_dict[key][0]] + sex_dict[feature_dict[key][1]] + rank_dict[feature_dict[key][2]] + [feature_dict[key][3]]
    return transfer_feature

'''获取商品特征字典{pID:{a1,a2,a3,cate,brand}}
a1:[-1,1,2,3]
a2:[-1,1,2]
a3:[-1,1,2]
'''
def product_feature():
    r_file = file('JData/JData_Product.csv', 'r')
    reader = csv.reader(r_file)
    feature_dict = {}
    a1_dict = {'-1': [1,0,0,0], '1': [0,1,0,0], '2': [0,0,1,0], '3': [0,0,0,1]}
    a2_dict = {'-1': [1,0,0], '1': [0,1,0], '2': [0,0,1]}
    a3_dict = {'-1': [1,0,0], '1': [0,1,0], '2': [0,0,1]}
    for line in reader:
        if reader.line_num == 1:
            continue
        feature_dict[line[0]] = a1_dict[line[1]] + a2_dict[line[2]] + a3_dict[line[3]] + [line[4]] + [line[5]]
    return feature_dict
def product_brand():
    I_brand_dict = dict()
    r_file = file('JData/JData_Product.csv', 'r')
    reader = csv.reader(r_file)
    for line in reader:
        if reader.line_num == 1:
            continue
        I_brand_dict[line[0]] = line[5]
    brand_set = np.sort(np.array(list(set(I_brand_dict.values())), int))
    transfer_dict = dict()
    for item in brand_set:
        length = len(str(bin(item))[2:])
        trans = '0' * (8-length) + str(bin(item))[2:]
        transfer_dict[item] = np.array(list(trans), int).tolist()
    return transfer_dict

'''按时间节点拆分评论行为'''
def write_comment_file():
    comm = pd.read_csv('JData/JData_Comment.csv', sep=',')
    name_lst = comm['dt'].unique()
    for item in name_lst:
        mon = int(item.split('-')[1])
        day = int(item.split('-')[2])
        comm[comm['dt'] == item].to_csv('Comment/'+str(mon)+'_'+str(day)+'.csv', sep=',')

'''获取商品评论特征字典{pID:[评论数，有无差评]}'''
def Comment_feature():
    r_file = file('JData/JData_Comment.csv', 'r')
    reader = csv.reader(r_file)
    comment_num = dict()
    has_bad_comment = dict()
    bad_comment_rate = dict()
    time_set = set()
    for line in reader:
        if reader.line_num == 1:
            continue
        time_set.add(line[0])
        if line[1] not in comment_num:
            comment_num[line[1]] = list()
        comment_num[line[1]].append(line[2])
        if line[1] not in has_bad_comment:
            has_bad_comment[line[1]] = list()
        has_bad_comment[line[1]].append(line[3])
        if line[1] not in bad_comment_rate:
            bad_comment_rate[line[1]] = list()
        bad_comment_rate[line[1]].append(line[4])
    #print time_set
    return comment_num, has_bad_comment, bad_comment_rate

'''商品评论变化趋势特征字典，返回：
    商品评论数trend字典：{商品ID：[11个时间节点的评论数]}，范围:[0,1,2,3,4]
    商品差评率trend字典：{商品ID：[11个时间节点的差评率]}，范围：[0.0,1.0]区间内浮点数
'''
def comment_trend():
    comm_num_trend_dict = {}
    bad_comm_trend_dict = {}
    file_name_dict = {0: '2_1', 1: '2_8', 2: '2_15', 3: '2_22', 4: '2_29', 5: '3_7', 6: '3_14', 7: '3_21', 8: '3_28', 9: '4_4', 10: '4_11', 11: '4_15'}
    for key in file_name_dict:
        r_file = file('Comment/' + file_name_dict[key] + '.csv', 'r')
        reader = csv.reader(r_file)
        for line in reader:
            if reader.line_num == 1:
                continue
            if line[2] not in comm_num_trend_dict:
                comm_num_trend_dict[line[2]] = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
            comm_num_trend_dict[line[2]][key] = line[3]
            if line[2] not in bad_comm_trend_dict:
                bad_comm_trend_dict[line[2]] = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]
            bad_comm_trend_dict[line[2]][key] = line[5]
    return comm_num_trend_dict, bad_comm_trend_dict

'''统计用户注册时间：{2016年以前：[1,0,0,0,0], 2016年1月：[0,1,0,0,0], 2月：[0,0,1,0,0], 3月：[0,0,0,1,0], 4月：[0,0,0,0,1]}'''
def signup_time_dict():
    r_file = file('JData/JData_User.csv', 'r')
    reader = csv.reader(r_file)
    feature_dict = {}
    for line in reader:
        if reader.line_num == 1:
            continue
        year = line[-1].split('-')[0]
        # print year
        if year != '2016':
            feature_dict[line[0]] = [1, 0, 0, 0, 0, 0]
        else:
            month = line[-1].split('-')[1]
            if int(month) == 1:
                feature_dict[line[0]] = [0, 1, 0, 0, 0, 0]
            elif int(month) == 2:
                feature_dict[line[0]] = [0, 0, 1, 0, 0, 0]
            elif int(month) == 3:
                feature_dict[line[0]] = [0, 0, 0, 1, 0, 0]
            elif int(month) == 4:
                feature_dict[line[0]] = [0, 0, 0, 0, 1, 0]
            else:
                feature_dict[line[0]] = [0, 0, 0, 0, 0, 1]
    return feature_dict

if __name__ == '__main__':
    print 'get feature dict!'
    # comm_feat = Comment_feature()
    # ergodic_dict(comm_feat, num=5)
    #signup_feat = signup_time_dict()
    #ergodic_dict(signup_feat, num=200)
    #print set(np.array(product_feature().values())[:, 4])
    #product_brand()
