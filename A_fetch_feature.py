# -*- coding:UTF-8 -*-
"""
2月：1-29
3月：30-60
4月：61-75
验证：69-73
"""
import csv
import A_info_dict
import random
import numpy as np
import pandas as pd
'''
预测天：start_day+1～start_day+5
使用UI对：start_day～start_day-9中出现的UI对
使用数据：start_day～start_day-20
'''
DAY = 'Day'
NewDay = 'NewDay'
weekend_set = {6, 7, 13, 14, 20, 21, 27, 28, 34, 35, 41, 42, 48, 49, 55, 56, 62, 63, 69, 70}
new_windows = {61, 54, 47, 40, 33}
def get_feature(start_day, state='train'):
    pred_end_day = start_day+5
    set_end_day = start_day-10
    feat_end_day = start_day-50
###########定义特征字典#########################################
    U_action_TF = dict()
    I_action_TF = dict()
    All_feat = dict()
    U_day5 = dict()
    U_day10 = dict()
    U_day20 = dict()
    U_day30 = dict()
    U_day40 = dict()
    U_day50 = dict()
    U_scan_day5 = dict()
    U_scan_day10 = dict()
    U_scan_day20 = dict()
    U_scan_day30 = dict()
    U_scan_day40 = dict()
    U_scan_day50 = dict()
    U_cart_day5 = dict()
    U_cart_day10 = dict()
    U_cart_day20 = dict()
    U_cart_day30 = dict()
    U_cart_day40 = dict()
    U_cart_day50 = dict()
    U_kill_day5 = dict()
    U_kill_day10 = dict()
    U_kill_day20 = dict()
    U_kill_day30 = dict()
    U_kill_day40 = dict()
    U_kill_day50 = dict()
    U_buy_day5 = dict()
    U_buy_day10 = dict()
    U_buy_day20 = dict()
    U_buy_day30 = dict()
    U_buy_day40 = dict()
    U_buy_day50 = dict()
    U_follow_day5 = dict()
    U_follow_day10 = dict()
    U_follow_day20 = dict()
    U_follow_day30 = dict()
    U_follow_day40 = dict()
    U_follow_day50 = dict()
    U_click_day5 = dict()
    U_click_day10 = dict()
    U_click_day20 = dict()
    U_click_day30 = dict()
    U_click_day40 = dict()
    U_click_day50 = dict()
    ##########用户行为###########
    U_action_1st_day = dict()
    U_action_2nd_day = dict()
    U_action_3rd_day = dict()
    U_action_2_days = dict()
    U_action_4_days = dict()
    U_action_6_days = dict()
    U_action_3_days = dict()
    U_action_5_days = dict()
    U_action_10_days = dict()
    U_action_1st_week = dict()
    U_action_2nd_week = dict()
    U_action_3rd_week = dict()
    U_action_4th_week = dict()
    U_action_2_weeks = dict()
    U_action_3_weeks = dict()
    U_action_4_weeks = dict()
    U_action_40_days = dict()
    U_action_50_days = dict()
    ##########商品行为###########
    I_action_1st_day = dict()
    I_action_2nd_day = dict()
    I_action_3rd_day = dict()
    I_action_3_days = dict()
    I_action_5_days = dict()
    I_action_10_days = dict()
    I_action_1st_week = dict()
    I_action_2nd_week = dict()
    I_action_3rd_week = dict()
    I_action_4th_week = dict()
    I_action_2_weeks = dict()
    I_action_3_weeks = dict()
    I_action_4_weeks = dict()
    I_action_40_days = dict()
    I_action_50_days = dict()
    I_action_2_days = dict()
    I_action_4_days = dict()
    I_action_6_days = dict()
    ########用户-商品对行为########
    UI_action_1st_day = dict()
    UI_action_2nd_day = dict()
    UI_action_3rd_day = dict()
    UI_action_3_days = dict()
    UI_action_5_days = dict()
    UI_action_10_days = dict()
    UI_action_1st_week = dict()
    UI_action_2nd_week = dict()
    UI_action_3rd_week = dict()
    UI_action_4th_week = dict()
    UI_action_2_weeks = dict()
    UI_action_3_weeks = dict()
    UI_action_4_weeks = dict()
    UI_action_40_days = dict()
    UI_action_50_days = dict()
    UI_action_2_days = dict()
    UI_action_4_days = dict()
    UI_action_6_days = dict()
    ########10天中用户购物车/收藏夹深度########
    U_cart_depth3 = dict()
    U_follow_depth3 = dict()
    U_cart_depth5 = dict()
    U_follow_depth5 = dict()
    U_cart_depth10 = dict()
    U_follow_depth10 = dict()
    U_cart_depth20 = dict()
    U_follow_depth20 = dict()
    U_cart_depth30 = dict()
    U_follow_depth30 = dict()
    U_cart_depth40 = dict()
    U_follow_depth40 = dict()
    U_cart_depth50 = dict()
    U_follow_depth50 = dict()
###########遍历前10天，获取UI集合################################
    U_set = set()
    I_set = set()
    UI_set = set()
    All_U_set = set()
    All_I_set = set()
    All_UI_set = set()
    IB_dict = dict()
    for i in range(start_day, feat_end_day, -1):
        file_name = DAY + '/%s.csv' % (str(i))
        r_file = file(file_name, 'r')
        reader = csv.reader(r_file)
        for line in reader:
            All_U_set.add(line[0])
            All_I_set.add(line[1])
            All_UI_set.add((line[0], line[1]))
            IB_dict[line[1]] = line[4]
            if i > set_end_day:
                U_set.add(line[0])
                I_set.add(line[1])
                UI_set.add((line[0], line[1]))
###########特征字典初始化#########################################
    for item in U_set:
        U_cart_depth3[item] = set()
        U_follow_depth3[item] = set()
        U_cart_depth5[item] = set()
        U_follow_depth5[item] = set()
        U_cart_depth10[item] = set()
        U_follow_depth10[item] = set()
        U_action_TF[item] = 50 * [0]
    for item in All_U_set:
        U_cart_depth20[item] = set()
        U_follow_depth20[item] = set()
        U_cart_depth30[item] = set()
        U_follow_depth30[item] = set()
        U_cart_depth40[item] = set()
        U_follow_depth40[item] = set()
        U_cart_depth50[item] = set()
        U_follow_depth50[item] = set()
    U_element_num = 6
    I_element_num = 6
    UI_element_num = 6
    for elem in U_set:
        U_action_1st_day[elem] = U_element_num *[0]
        U_action_2nd_day[elem] = U_element_num *[0]
        U_action_3rd_day[elem] = U_element_num *[0]
        U_action_3_days[elem] = U_element_num *[0]
        U_action_5_days[elem] = U_element_num * [0]
        U_action_10_days[elem] = U_element_num * [0]
        U_action_1st_week[elem] = U_element_num *[0]
        U_action_2_days[elem] = U_element_num *[0]
        U_action_4_days[elem] = U_element_num *[0]
        U_action_6_days[elem] = U_element_num *[0]
        U_day5[elem] = set()
        U_day10[elem] = set()
        U_scan_day5[elem] = set()
        U_scan_day10[elem] = set()
        U_cart_day5[elem] = set()
        U_cart_day10[elem] = set()
        U_kill_day5[elem] = set()
        U_kill_day10[elem] = set()
        U_buy_day5[elem] = set()
        U_buy_day10[elem] = set()
        U_follow_day5[elem] = set()
        U_follow_day10[elem] = set()
        U_click_day5[elem] = set()
        U_click_day10[elem] = set()
    for elem in All_U_set:
        U_action_2nd_week[elem] = U_element_num * [0]
        U_action_2_weeks[elem] = U_element_num * [0]
        U_action_3rd_week[elem] = U_element_num * [0]
        U_action_3_weeks[elem] = U_element_num * [0]
        U_day20[elem] = set()
        U_scan_day20[elem] = set()
        U_cart_day20[elem] = set()
        U_kill_day20[elem] = set()
        U_buy_day20[elem] = set()
        U_follow_day20[elem] = set()
        U_click_day20[elem] = set()
        U_action_4th_week[elem] = U_element_num * [0]
        U_action_4_weeks[elem] = U_element_num * [0]
        U_action_40_days[elem] = U_element_num * [0]
        U_action_50_days[elem] = U_element_num * [0]
        U_day30[elem] = set()
        U_day40[elem] = set()
        U_day50[elem] = set()
        U_scan_day30[elem] = set()
        U_scan_day40[elem] = set()
        U_scan_day50[elem] = set()
        U_cart_day30[elem] = set()
        U_cart_day40[elem] = set()
        U_cart_day50[elem] = set()
        U_kill_day30[elem] = set()
        U_kill_day40[elem] = set()
        U_kill_day50[elem] = set()
        U_buy_day30[elem] = set()
        U_buy_day40[elem] = set()
        U_buy_day50[elem] = set()
        U_follow_day30[elem] = set()
        U_follow_day40[elem] = set()
        U_follow_day50[elem] = set()
        U_click_day30[elem] = set()
        U_click_day40[elem] = set()
        U_click_day50[elem] = set()
    for elem in I_set:
        I_action_1st_day[elem] = I_element_num * [0]
        I_action_2nd_day[elem] = I_element_num * [0]
        I_action_3rd_day[elem] = I_element_num * [0]
        I_action_10_days[elem] = I_element_num * [0]
        I_action_3_days[elem] = I_element_num * [0]
        I_action_5_days[elem] = I_element_num * [0]
        I_action_1st_week[elem] = I_element_num * [0]
        I_action_TF[item] = 50 * [0]
        I_action_2_days[elem] = I_element_num * [0]
        I_action_4_days[elem] = I_element_num * [0]
        I_action_6_days[elem] = I_element_num * [0]
    for elem in All_I_set:
        I_action_2nd_week[elem] = I_element_num * [0]
        I_action_2_weeks[elem] = I_element_num * [0]
        I_action_3rd_week[elem] = I_element_num * [0]
        I_action_3_weeks[elem] = I_element_num * [0]
        I_action_4th_week[elem] = I_element_num * [0]
        I_action_4_weeks[elem] = I_element_num * [0]
        I_action_40_days[elem] = I_element_num * [0]
        I_action_50_days[elem] = I_element_num * [0]
    for elem in UI_set:
        UI_action_1st_day[elem] = UI_element_num * [0]
        UI_action_2nd_day[elem] = UI_element_num * [0]
        UI_action_3rd_day[elem] = UI_element_num * [0]
        UI_action_3_days[elem] = UI_element_num * [0]
        UI_action_5_days[elem] = UI_element_num * [0]
        UI_action_10_days[elem] = UI_element_num * [0]
        UI_action_1st_week[elem] = UI_element_num * [0]
        UI_action_2_days[elem] = UI_element_num * [0]
        UI_action_4_days[elem] = UI_element_num * [0]
        UI_action_6_days[elem] = UI_element_num * [0]
    for elem in All_UI_set:
        UI_action_2nd_week[elem] = UI_element_num * [0]
        UI_action_2_weeks[elem] = UI_element_num * [0]
        UI_action_3rd_week[elem] = UI_element_num * [0]
        UI_action_3_weeks[elem] = UI_element_num * [0]
        UI_action_4th_week[elem] = UI_element_num * [0]
        UI_action_4_weeks[elem] = UI_element_num * [0]
        UI_action_40_days[elem] = UI_element_num * [0]
        UI_action_50_days[elem] = UI_element_num * [0]
##########遍历前21天，获取特征###################################
    ######用户最后加购的商品###########
    last_cart_dict = dict()
    last_follow_dict = dict()
    last_buy_dict = dict()
    last_killcart_dict = dict()
    last_click_dict = dict()
    alpha = 0
    for i in range(start_day, feat_end_day, -1):
        dis_day = start_day - i
        # print 'Day:', dis_day
        file_name = DAY + '/%s.csv' % (str(i))
        r_file = file(file_name, 'r')
        reader = csv.reader(r_file)
        decay = 1.0 #/ (1.0 + alpha * dis_day)
        for line in reader:
            if (dis_day < 10):
                U_action_TF[line[0]][dis_day] = 1
                #I_action_TF[line[1]][dis_day] = 1
                U_action_10_days[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_10_days[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_10_days[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
                U_day10[line[0]].add(dis_day)
                if line[2] == '1':
                    U_scan_day10[line[0]].add(dis_day)
                if line[2] == '2':
                    U_cart_depth10[line[0]].add(line[1])
                    U_cart_day10[line[0]].add(dis_day)
                if line[2] == '3':
                    U_kill_day10[line[0]].add(dis_day)
                    if line[1] in U_cart_depth10[line[0]]:
                        U_cart_depth10[line[0]].remove(line[1])
                if line[2] == '4':
                    U_buy_day10[line[0]].add(dis_day)
                if line[2] == '5':
                    U_follow_day10[line[0]].add(dis_day)
                    U_follow_depth10[line[0]].add(line[1])
                if line[2] == '6':
                    U_click_day10[line[0]].add(dis_day)
            U_action_50_days[line[0]][int(line[2]) - 1] += 1.0 * decay
            I_action_50_days[line[1]][int(line[2]) - 1] += 1.0 * decay
            UI_action_50_days[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
            U_day50[line[0]].add(dis_day)
            if line[2] == '1':
                U_scan_day50[line[0]].add(dis_day)
            if line[2] == '2':
                U_cart_day50[line[0]].add(dis_day)
                U_cart_depth50[line[0]].add(line[1])
            if line[2] == '3':
                U_kill_day50[line[0]].add(dis_day)
            if line[2] == '4':
                U_buy_day50[line[0]].add(dis_day)
                if line[1] in U_cart_depth50:
                    U_cart_depth50[line[0]].remove(line[1])
            if line[2] == '5':
                U_follow_day50[line[0]].add(dis_day)
                U_follow_depth50[line[0]].add(line[1])
            if line[2] == '6':
                U_click_day50[line[0]].add(dis_day)
            ####################前40天#####################
            if dis_day < 40:
                U_action_40_days[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_40_days[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_40_days[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
                U_day40[line[0]].add(dis_day)
                if line[2] == '1':
                    U_scan_day40[line[0]].add(dis_day)
                if line[2] == '2':
                    U_cart_day40[line[0]].add(dis_day)
                    U_cart_depth40[line[0]].add(line[1])
                if line[2] == '3':
                    U_kill_day40[line[0]].add(dis_day)
                    if line[1] in U_cart_depth40:
                        U_cart_depth40[line[0]].remove(line[1])
                if line[2] == '4':
                    U_buy_day40[line[0]].add(dis_day)
                if line[2] == '5':
                    U_follow_day40[line[0]].add(dis_day)
                    U_follow_depth40[line[0]].add(line[1])
                if line[2] == '6':
                    U_click_day40[line[0]].add(dis_day)
            if dis_day < 30:
                U_day30[line[0]].add(dis_day)
                if line[2] == '1':
                    U_scan_day30[line[0]].add(dis_day)
                if line[2] == '2':
                    U_cart_day30[line[0]].add(dis_day)
                    U_cart_depth30[line[0]].add(line[1])
                if line[2] == '3':
                    U_kill_day30[line[0]].add(dis_day)
                    if line[1] in U_cart_depth30:
                        U_cart_depth30[line[0]].remove(line[1])
                if line[2] == '4':
                    U_buy_day30[line[0]].add(dis_day)
                if line[2] == '5':
                    U_follow_day30[line[0]].add(dis_day)
                    U_follow_depth30[line[0]].add(line[1])
                if line[2] == '6':
                    U_click_day30[line[0]].add(dis_day)
            if dis_day < 20:
                U_day20[line[0]].add(dis_day)
                if line[2] == '1':
                    U_scan_day20[line[0]].add(dis_day)
                if line[2] == '2':
                    U_cart_day20[line[0]].add(dis_day)
                    U_cart_depth20[line[0]].add(line[1])
                if line[2] == '3':
                    U_kill_day20[line[0]].add(dis_day)
                    if line[1] in U_cart_depth20:
                        U_cart_depth20[line[0]].remove(line[1])
                if line[2] == '4':
                    U_buy_day20[line[0]].add(dis_day)
                if line[2] == '5':
                    U_follow_day20[line[0]].add(dis_day)
                    U_follow_depth20[line[0]].add(line[1])
                if line[2] == '6':
                    U_click_day20[line[0]].add(dis_day)
            ####################全部4周#####################
            if dis_day < 28:
                U_action_4_weeks[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_4_weeks[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_4_weeks[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
                if dis_day >= 21:
                    U_action_4th_week[line[0]][int(line[2]) - 1] += 1.0 * decay
                    I_action_4th_week[line[1]][int(line[2]) - 1] += 1.0 * decay
                    UI_action_4th_week[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
            ####################全部3周#####################
            if dis_day < 21:
                U_action_3_weeks[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_3_weeks[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_3_weeks[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
                if dis_day >= 14:
                    U_action_3rd_week[line[0]][int(line[2]) - 1] += 1.0 * decay
                    I_action_3rd_week[line[1]][int(line[2]) - 1] += 1.0 * decay
                    UI_action_3rd_week[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
            ####################全部2周#####################
            if dis_day < 14:
                U_action_2_weeks[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_2_weeks[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_2_weeks[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
                if dis_day >= 7:
                    U_action_2nd_week[line[0]][int(line[2]) - 1] += 1.0 * decay
                    I_action_2nd_week[line[1]][int(line[2]) - 1] += 1.0 * decay
                    UI_action_2nd_week[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
            ####################第1天#######################
            if dis_day == 0:
                U_action_1st_day[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_1st_day[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_1st_day[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
            ####################第2天#######################
            if dis_day == 1:
                U_action_2nd_day[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_2nd_day[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_2nd_day[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
            ####################第3天#######################
            if dis_day == 2:
                U_action_3rd_day[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_3rd_day[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_3rd_day[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
            ####################前3天#######################
            if dis_day < 3:
                U_action_3_days[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_3_days[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_3_days[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
                ##################最后操作######################
                if (line[2] == '2') and (line[0] not in last_cart_dict):
                    last_cart_dict[line[0]] = line[1]
                    U_cart_depth3[line[0]].add(line[1])
                if (line[2] == '3') and (line[0] not in last_killcart_dict):
                    last_killcart_dict[line[0]] = line[1]
                    if line[1] in U_cart_depth3:
                        U_cart_depth3[line[0]].remove(line[1])
                if (line[2] == '4') and (line[0] not in last_buy_dict):
                    last_buy_dict[line[0]] = line[1]
                if (line[2] == '5') and (line[0] not in last_follow_dict):
                    last_follow_dict[line[0]] = line[1]
                    U_follow_depth3[line[0]].add(line[1])
                if (line[2] == '6') and (line[0] not in last_click_dict):
                    last_click_dict[line[0]] = line[1]
            ####################前5天#######################
            if dis_day < 5:
                U_action_5_days[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_5_days[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_5_days[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
                U_day5[line[0]].add(dis_day)
                if line[2] == '1':
                    U_scan_day5[line[0]].add(dis_day)
                if line[2] == '2':
                    U_cart_day5[line[0]].add(dis_day)
                    U_cart_depth5[line[0]].add(line[1])
                if line[2] == '3':
                    U_kill_day5[line[0]].add(dis_day)
                    if line[1] in U_cart_depth5:
                        U_cart_depth5[line[0]].remove(line[1])
                if line[2] == '4':
                    U_buy_day5[line[0]].add(dis_day)
                if line[2] == '5':
                    U_follow_day5[line[0]].add(dis_day)
                    U_follow_depth5[line[0]].add(line[1])
                if line[2] == '6':
                    U_click_day5[line[0]].add(dis_day)
            ####################前6天#######################
            if dis_day < 6:
                U_action_6_days[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_6_days[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_6_days[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
            ####################前4天#######################
            if dis_day < 4:
                U_action_4_days[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_4_days[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_4_days[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
            ####################前2天#######################
            if dis_day < 2:
                U_action_2_days[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_2_days[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_2_days[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
            ####################第1周#######################
            if dis_day < 7:
                U_action_1st_week[line[0]][int(line[2]) - 1] += 1.0 * decay
                I_action_1st_week[line[1]][int(line[2]) - 1] += 1.0 * decay
                UI_action_1st_week[(line[0], line[1])][int(line[2]) - 1] += 1.0 * decay
###########合并特征################################################
    usr_feat = A_info_dict.usr_feature()
    product_feat = A_info_dict.product_feature()
    comment_num, has_bad_comment, bad_comment_rate = A_info_dict.Comment_feature()
    brand_feature = A_info_dict.product_brand()
    for elem in UI_set:
        if elem[1] not in comment_num:
            comment_num[elem[1]] = [-1] * 12
        if elem[1] not in has_bad_comment:
            has_bad_comment[elem[1]] = [-1] * 12
        if elem[1] not in bad_comment_rate:
            bad_comment_rate[elem[1]] = [-1] * 12
        last_action = [0,0,0,0,0]
        if (elem[0] in last_cart_dict) and (elem[1] == last_cart_dict[elem[0]]):
            last_action[0] = 1
        if (elem[0] in last_killcart_dict) and (elem[1] == last_killcart_dict[elem[0]]):
            last_action[1] = 1
        if (elem[0] in last_buy_dict) and (elem[1] == last_buy_dict[elem[0]]):
            last_action[2] = 1
        if (elem[0] in last_follow_dict) and (elem[1] == last_follow_dict[elem[0]]):
            last_action[3] = 1
        if (elem[0] in last_click_dict) and (elem[1] == last_click_dict[elem[0]]):
            last_action[4] = 1
        Urate1 = [U_action_1st_week[elem[0]][0] / (1+U_action_1st_week[elem[0]][3])] + \
                [U_action_1st_week[elem[0]][1] / (1+U_action_1st_week[elem[0]][3])] + \
                [U_action_1st_week[elem[0]][2] / (1+U_action_1st_week[elem[0]][3])] + \
                [U_action_1st_week[elem[0]][4] / (1+U_action_1st_week[elem[0]][3])] + \
                [U_action_1st_week[elem[0]][5] / (1+U_action_1st_week[elem[0]][3])]
        Urate2 = [U_action_10_days[elem[0]][0] / (1 + U_action_10_days[elem[0]][3])] + \
                [U_action_10_days[elem[0]][1] / (1 + U_action_10_days[elem[0]][3])] + \
                [U_action_10_days[elem[0]][2] / (1 + U_action_10_days[elem[0]][3])] + \
                [U_action_10_days[elem[0]][4] / (1 + U_action_10_days[elem[0]][3])] + \
                [U_action_10_days[elem[0]][5] / (1 + U_action_10_days[elem[0]][3])]
        Urate3 = [U_action_4_weeks[elem[0]][0] / (1 + U_action_4_weeks[elem[0]][3])] + \
                 [U_action_4_weeks[elem[0]][1] / (1 + U_action_4_weeks[elem[0]][3])] + \
                 [U_action_4_weeks[elem[0]][2] / (1 + U_action_4_weeks[elem[0]][3])] + \
                 [U_action_4_weeks[elem[0]][4] / (1 + U_action_4_weeks[elem[0]][3])] + \
                 [U_action_4_weeks[elem[0]][5] / (1 + U_action_4_weeks[elem[0]][3])]
        Irate1 = [I_action_1st_week[elem[1]][0] / (1+I_action_1st_week[elem[1]][3])] + \
                [I_action_1st_week[elem[1]][1] / (1+I_action_1st_week[elem[1]][3])] + \
                [I_action_1st_week[elem[1]][2] / (1+I_action_1st_week[elem[1]][3])] + \
                [I_action_1st_week[elem[1]][4] / (1+I_action_1st_week[elem[1]][3])] + \
                [I_action_1st_week[elem[1]][5] / (1+I_action_1st_week[elem[1]][3])]
        Irate2 = [I_action_10_days[elem[1]][0] / (1 + I_action_10_days[elem[1]][3])] + \
                [I_action_10_days[elem[1]][1] / (1 + I_action_10_days[elem[1]][3])] + \
                [I_action_10_days[elem[1]][2] / (1 + I_action_10_days[elem[1]][3])] + \
                [I_action_10_days[elem[1]][4] / (1 + I_action_10_days[elem[1]][3])] + \
                [I_action_10_days[elem[1]][5] / (1 + I_action_10_days[elem[1]][3])]
        Irate3 = [I_action_4_weeks[elem[1]][0] / (1 + I_action_4_weeks[elem[1]][3])] + \
                 [I_action_4_weeks[elem[1]][1] / (1 + I_action_4_weeks[elem[1]][3])] + \
                 [I_action_4_weeks[elem[1]][2] / (1 + I_action_4_weeks[elem[1]][3])] + \
                 [I_action_4_weeks[elem[1]][4] / (1 + I_action_4_weeks[elem[1]][3])] + \
                 [I_action_4_weeks[elem[1]][5] / (1 + I_action_4_weeks[elem[1]][3])]
        sum_action = [sum(U_action_1st_day[elem[0]])] + [sum(U_action_2nd_day[elem[0]])] + [sum(U_action_3rd_day[elem[0]])] + \
                     [sum(U_action_3_days[elem[0]])] + [sum(U_action_1st_week[elem[0]])] + [sum(U_action_4_weeks[elem[0]])] + \
                     [sum(U_action_2_weeks[elem[0]])] + [sum(U_action_3_weeks[elem[0]])] + \
                     [sum(I_action_1st_day[elem[1]])] + [sum(I_action_2nd_day[elem[1]])] + [sum(I_action_3rd_day[elem[1]])] + \
                         [sum(I_action_3_days[elem[1]])] + [sum(I_action_1st_week[elem[1]])] + [sum(I_action_4_weeks[elem[1]])] + \
                     [sum(I_action_2_weeks[elem[1]])] + [sum(I_action_3_weeks[elem[1]])] + \
                     [sum(UI_action_1st_day[elem])] + [sum(UI_action_2nd_day[elem])] + [sum(UI_action_3rd_day[elem])] + \
                         [sum(UI_action_3_days[elem])] + [sum(UI_action_1st_week[elem])] + [sum(UI_action_4_weeks[elem])] + \
                     [sum(UI_action_2_weeks[elem])] + [sum(UI_action_3_weeks[elem])] + \
                     [sum(U_action_40_days[elem[0]])] + [sum(I_action_40_days[elem[1]])] + [sum(UI_action_40_days[elem])] + \
                     [sum(U_action_50_days[elem[0]])] + [sum(I_action_50_days[elem[1]])] + [sum(UI_action_50_days[elem])]

        cart_follow_sumU = [U_action_1st_day[elem[0]][1]+U_action_1st_day[elem[0]][4]] + \
                           [U_action_2nd_day[elem[0]][1] + U_action_2nd_day[elem[0]][4]] + \
                           [U_action_3rd_day[elem[0]][1] + U_action_3rd_day[elem[0]][4]] + \
                           [U_action_3_days[elem[0]][1] + U_action_3_days[elem[0]][4]] + \
                           [U_action_1st_week[elem[0]][1] + U_action_1st_week[elem[0]][4]] + \
                           [U_action_2_weeks[elem[0]][1] + U_action_2_weeks[elem[0]][4]] + \
                           [U_action_3_weeks[elem[0]][1] + U_action_3_weeks[elem[0]][4]] + \
                           [U_action_4_weeks[elem[0]][1] + U_action_4_weeks[elem[0]][4]] + \
                           [U_action_40_days[elem[0]][1] + U_action_40_days[elem[0]][4]] + \
                           [U_action_50_days[elem[0]][1] + U_action_50_days[elem[0]][4]]

        kill_buy_sumU = [U_action_1st_day[elem[0]][2] + U_action_1st_day[elem[0]][3]] + \
                        [U_action_2nd_day[elem[0]][2] + U_action_2nd_day[elem[0]][3]] + \
                        [U_action_3rd_day[elem[0]][2] + U_action_3rd_day[elem[0]][3]] + \
                        [U_action_3_days[elem[0]][2] + U_action_3_days[elem[0]][3]] + \
                           [U_action_1st_week[elem[0]][2] + U_action_1st_week[elem[0]][3]] + \
                           [U_action_2_weeks[elem[0]][2] + U_action_2_weeks[elem[0]][3]] + \
                           [U_action_3_weeks[elem[0]][2] + U_action_3_weeks[elem[0]][3]] + \
                           [U_action_4_weeks[elem[0]][2] + U_action_4_weeks[elem[0]][3]] + \
                           [U_action_40_days[elem[0]][2] + U_action_40_days[elem[0]][3]] + \
                           [U_action_50_days[elem[0]][2] + U_action_50_days[elem[0]][3]]

        cart_follow_sumI = [I_action_1st_day[elem[1]][1] + I_action_1st_day[elem[1]][4]] + \
                           [I_action_2nd_day[elem[1]][1] + I_action_2nd_day[elem[1]][4]] + \
                           [I_action_3rd_day[elem[1]][1] + I_action_3rd_day[elem[1]][4]] + \
                           [I_action_3_days[elem[1]][1] + I_action_3_days[elem[1]][4]] + \
                           [I_action_1st_week[elem[1]][1] + I_action_1st_week[elem[1]][4]] + \
                           [I_action_2_weeks[elem[1]][1] + I_action_2_weeks[elem[1]][4]] + \
                           [I_action_3_weeks[elem[1]][1] + I_action_3_weeks[elem[1]][4]] + \
                           [I_action_4_weeks[elem[1]][1] + I_action_4_weeks[elem[1]][4]] + \
                           [I_action_40_days[elem[1]][1] + I_action_40_days[elem[1]][4]] + \
                           [I_action_50_days[elem[1]][1] + I_action_50_days[elem[1]][4]]

        if elem[1] not in brand_feature:
            brand_feature[elem[1]] = [0,0,0,0,0,0,0,0]
        U_day = [len(U_day5[elem[0]])] + [len(U_day10[elem[0]])] +[len(U_day20[elem[0]])] + [len(U_day30[elem[0]])] + [len(U_day40[elem[0]])] + [len(U_day50[elem[0]])]

        All_feat[elem] = U_action_1st_day[elem[0]] + U_action_2nd_day[elem[0]] + U_action_3rd_day[elem[0]] + \
                            U_action_3_days[elem[0]] + U_action_5_days[elem[0]] + U_action_10_days[elem[0]] + U_action_1st_week[elem[0]] + \
                         U_action_2_weeks[elem[0]] + U_action_3_weeks[elem[0]] + U_action_4_weeks[elem[0]] + \
                         I_action_1st_day[elem[1]] + I_action_2nd_day[elem[1]] + I_action_3rd_day[elem[1]] + \
                            I_action_3_days[elem[1]] + I_action_5_days[elem[1]] + I_action_10_days[elem[1]] + I_action_1st_week[elem[1]] + \
                         I_action_2_weeks[elem[1]] + I_action_3_weeks[elem[1]] + I_action_4_weeks[elem[1]] + \
                         UI_action_1st_day[elem] + UI_action_2nd_day[elem] + UI_action_3rd_day[elem] + \
                            UI_action_3_days[elem] + UI_action_5_days[elem] + UI_action_10_days[elem] + UI_action_1st_week[elem] + \
                         UI_action_2_weeks[elem] + UI_action_3_weeks[elem] + UI_action_4_weeks[elem] + \
                         U_action_40_days[elem[0]] + I_action_40_days[elem[1]] + UI_action_40_days[elem] + \
                         U_action_50_days[elem[0]] + I_action_50_days[elem[1]] + UI_action_50_days[elem] + \
                            usr_feat[elem[0]] + product_feat[elem[1]][:-2] + last_action + Urate1 + Irate1 + Urate2 + Irate2 + Urate3 + Irate3 + \
                         sum_action + [len(U_cart_depth10[elem[0]])] + [len(U_follow_depth10[elem[0]])] + \
                         comment_num[elem[1]] + has_bad_comment[elem[1]] + bad_comment_rate[elem[1]] + brand_feature[elem[1]] + \
                         cart_follow_sumU + U_day + cart_follow_sumI + kill_buy_sumU + \
                         U_action_TF[elem[0]] + \
                         (np.array(U_action_1st_day[elem[0]]) - np.array(U_action_2nd_day[elem[0]])).tolist() + \
                         (np.array(U_action_2nd_day[elem[0]]) - np.array(U_action_3rd_day[elem[0]])).tolist() + \
                         (np.array(I_action_1st_day[elem[1]]) - np.array(I_action_2nd_day[elem[1]])).tolist() + \
                         (np.array(I_action_2nd_day[elem[1]]) - np.array(I_action_3rd_day[elem[1]])).tolist() + \
                         (2 * np.array(U_action_1st_week[elem[0]]) - np.array(U_action_2_weeks[elem[0]])).tolist() + \
                         (2 * np.array(I_action_1st_week[elem[1]]) - np.array(I_action_2_weeks[elem[1]])).tolist()
            #U_action_2nd_week[elem[0]] + U_action_3rd_week[elem[0]] + U_action_4th_week[elem[0]] + \
                         #I_action_2nd_week[elem[1]] + I_action_3rd_week[elem[1]] + I_action_4th_week[elem[1]] + \
                         #UI_action_2nd_week[elem] + UI_action_3rd_week[elem] + UI_action_4th_week[elem]

            # + cart_follow_sumI + U_day + U_scan_day + U_cart_day + U_kill_day + U_buy_day + U_follow_day + U_click_day

                         #UB_action_1st_day[(elem[0], IB_dict[elem[1]])] + UB_action_2nd_day[(elem[0], IB_dict[elem[1]])] + UB_action_3rd_day[(elem[0], IB_dict[elem[1]])] + \
                         #UB_action_3_days[(elem[0], IB_dict[elem[1]])] + UB_action_5_days[(elem[0], IB_dict[elem[1]])] + UB_action_10_days[(elem[0], IB_dict[elem[1]])] + UB_action_1st_week[
                         #(elem[0], IB_dict[elem[1]])] + UB_action_2nd_week[(elem[0], IB_dict[elem[1]])] + \
                         #UB_action_3rd_week[(elem[0], IB_dict[elem[1]])] + UB_action_4th_week[(elem[0], IB_dict[elem[1]])] + UB_action_4_weeks[(elem[0], IB_dict[elem[1]])] + \
                         #UB_action_40_days[(elem[0], IB_dict[elem[1]])] + UB_action_50_days[(elem[0], IB_dict[elem[1]])]

            #[len(UI_scan_day[elem])] + [len(UI_cart_day[elem])] + [len(UI_killcart_day[elem])] + \
                         #[len(UI_buy_day[elem])] + [len(UI_follow_day[elem])] + [len(UI_click_day[elem])]
                         #[len(U_scan_day[elem[0]])] + [len(U_cart_day[elem[0]])] + [len(U_killcart_day[elem[0]])] + \
                         #[len(U_buy_day[elem[0]])] + [len(U_follow_day[elem[0]])] + [len(U_click_day[elem[0]])] + \
                         #[len(I_scan_day[elem[1]])] + [len(I_cart_day[elem[1]])] + [len(I_killcart_day[elem[1]])] + \
                         #[len(I_buy_day[elem[1]])] + [len(I_follow_day[elem[1]])] + [len(I_click_day[elem[1]])] + \
                         #[len(U_cart_depth[elem[0]])] + [len(U_follow_depth[elem[0]])] + \
                         #[len(UI_cart_day[elem]) / math.exp(len(UI_buy_day[elem]))] + \
                         #[len(UI_killcart_day[elem]) / math.exp(len(UI_buy_day[elem]))] + \
                         #[len(UI_follow_day[elem]) / math.exp(len(UI_buy_day[elem]))] + \
                         #[len(UI_click_day[elem]) / math.exp(len(UI_buy_day[elem]))] + \
                         #[len(U_scan_day[elem[0]]) / math.exp(len(U_buy_day[elem[0]]))] + \
                         #[len(U_cart_day[elem[0]]) / math.exp(len(U_buy_day[elem[0]]))] + \
                         #[len(U_killcart_day[elem[0]]) / math.exp(len(U_buy_day[elem[0]]))] + \
                         #[len(U_follow_day[elem[0]]) / math.exp(len(U_buy_day[elem[0]]))] + \
                         #[len(U_click_day[elem[0]]) / math.exp(len(U_buy_day[elem[0]]))] + \
                         #[len(I_scan_day[elem[1]]) / math.exp(len(I_buy_day[elem[1]]))] + \
                         #[len(I_cart_day[elem[1]]) / math.exp(len(I_buy_day[elem[1]]))] + \
                         #[len(I_killcart_day[elem[1]]) / math.exp(len(I_buy_day[elem[1]]))] + \
                         #[len(I_follow_day[elem[1]]) / math.exp(len(I_buy_day[elem[1]]))] + \
                         #[len(I_click_day[elem[1]]) / math.exp(len(I_buy_day[elem[1]]))]
        #[len(UI_scan_day[elem]) / math.exp(len(UI_buy_day[elem]))] + \#
    if state == 'train':
        UI_buy_set = set()
        pos_data = []
        neg_data = []
        for i in range(start_day+1, pred_end_day+1):
            file_name = DAY + '/%s.csv' % (str(i))
            r_file = file(file_name, 'r')
            reader = csv.reader(r_file)
            for line in reader:
                if line[2] == '4':
                    UI_buy_set.add((line[0], line[1]))
        for key in All_feat:
            if key in UI_buy_set:
                pos_data.append(All_feat[key])
            else:
                neg_data.append(All_feat[key])
        print 'UI_buy_set:', len(UI_buy_set)
        return pos_data, neg_data
    else:
        return All_feat

def get_data_by_slide_windows(start_day, windows, pos_file, neg_file):
    pos_data = []
    neg_data = []
    w_file_pos = file(pos_file, 'w')
    writer_pos = csv.writer(w_file_pos)
    w_file_neg = file(neg_file, 'w')
    writer_neg = csv.writer(w_file_neg)
    for i in range(windows):
        print 'Windows:', i
        pos_data, neg_data = get_feature(start_day+i, state='train')
        for line in pos_data:
            writer_pos.writerow(line)
        print len(pos_data)
        for line in neg_data:
            writer_neg.writerow(line)
        print len(neg_data)
    w_file_pos.close()
    w_file_neg.close()

def down_sample_neg_data(input_file, output_file, length_pos, rate):
    r_file = file(input_file, 'r')
    reader = csv.reader(r_file)
    neg_lst = []
    neg_select = []
    index = 0
    len_all = len(pd.read_csv(input_file))
    chu_shu = int(len_all / (length_pos*rate))
    yushu = int(random.uniform(0, chu_shu))
    for line in reader:
        #neg_lst.append(line)
        index += 1
        if index % chu_shu == yushu:
            #neg_select.extend(random.sample(neg_lst, 1))
            neg_select.append(line)
            #neg_lst = []
    r_file.close()
    #neg_select.extend(random.sample(neg_lst, 1))
    w_file = file(output_file, 'w')
    writer = csv.writer(w_file)
    for line in neg_select:
        writer.writerow(line)
    w_file.close()

def get_data(pos_file, neg_file):
    pos_data = []
    neg_data = []
    r_file = file(pos_file, 'r')
    reader = csv.reader(r_file)
    for line in reader:
        pos_data.append(line + [1])
    r_file.close()
    r_file = file(neg_file, 'r')
    reader = csv.reader(r_file)
    for line in reader:
        neg_data.append(line + [0])
    r_file.close()
    pos_data = pos_data
    print len(pos_data)
    print len(neg_data)
    #data = []
    #data.extend(pos_data)
    #data.extend(neg_data)
    np.random.seed(0)
    np.random.shuffle(pos_data)
    np.random.seed(1)
    np.random.shuffle(neg_data)

    len_pos = len(pos_data)
    len_neg = len(neg_data)
    train_pos = pos_data[:int(0.8 * len_pos)]
    test_pos = pos_data[int(0.8 * len_pos):]
    train_neg = neg_data[:int(0.8 * len_neg)]
    test_neg = neg_data[int(0.8 * len_neg):]

    train = []
    train.extend(train_pos)
    train.extend(train_neg)
    test = []
    test.extend(test_pos)
    test.extend(test_neg)

    np.random.seed(2)
    np.random.shuffle(train)
    np.random.seed(3)
    np.random.shuffle(test)

    train = np.array(train, float)
    test = np.array(test, float)

    train_data = train[:, :-1]
    train_label = train[:, -1]
    test_data = test[:,:-1]
    test_label = test[:,-1]
    return train_data, train_label, test_data, test_label


if __name__ == '__main__':
    print 'Fight back!!!'
    get_data_by_slide_windows(start_day=49, windows=15, pos_file='data/pos5_8.csv', neg_file='data/neg5_8.csv')
    #down_sample_neg_data(input_file='data/neg4_21new.csv', output_file='data/neg4_21new_down.csv', rate=100)
    #train_data, train_label = get_data(pos_file='data/pos4_21new.csv', neg_file='data/neg4_21new_down.csv')
    #print train_data[:5]
    #print train_label[:5]
