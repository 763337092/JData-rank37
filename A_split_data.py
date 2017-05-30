# -*- coding:UTF-8 -*-
import csv
import os
file_list = ['JData/JData_Action_201602.csv', 'JData/JData_Action_201603.csv', 'JData/JData_Action_201604.csv']

"""
    获取需要预测的所有商品id集合
"""
def get_sku_set():
    r_file = file('JData/JData_Product.csv', 'r')
    reader = csv.reader(r_file)
    sku_set = set()
    for line in reader:
        sku_set.add(line[0])

    return sku_set

def split_data():
    if not os.path.exists('Day'):
        os.mkdir('Day')

    w_name = []
    w_file = []
    w_writer = []
    for i in range(1, 76):
        w_name.append('Day/%s.csv' % (str(i)))
        w_file.append(file(w_name[i-1], 'w'))
        w_writer.append(csv.writer(w_file[i-1]))
    sku_set = get_sku_set()
    for n in range(len(file_list)):
        r_file = file(file_list[n], 'r')
        reader = csv.reader(r_file)
        result = {}
        print n
        if n == 0:
            for line in reader:
                if reader.line_num == 1:
                    continue
                day = int(line[2].split()[0].split('-')[2])
                if (line[1] in sku_set) and (day >= 1) and (day < 30):
                    w_writer[day-1].writerow([int(float(line[0])), line[1], line[4], line[5], line[6]])
            r_file.close()
        if n == 1:
            for line in reader:
                if reader.line_num == 1:
                    continue
                day = int(line[2].split()[0].split('-')[2]) + 29
                if (line[1] in sku_set) and (day >= 30) and (day <= 60):
                    w_writer[day - 1].writerow([int(float(line[0])), line[1], line[4], line[5], line[6]])
            r_file.close()
        if n == 2:
            for line in reader:
                if reader.line_num == 1:
                    continue
                day = int(line[2].split()[0].split('-')[2]) + 60
                if (line[1] in sku_set) and (day >= 61) and (day <= 75):
                    w_writer[day - 1].writerow([int(float(line[0])), line[1], line[4], line[5], line[6]])
            r_file.close()

if __name__ == '__main__':
    print ''
    split_data()