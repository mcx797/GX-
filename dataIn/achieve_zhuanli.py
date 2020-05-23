import xlrd
import os
import sys
import pymysql
import time
from datetime import datetime
from xlrd import xldate_as_tuple

path = 'data/achievement_zhuanli2.xlsx'


getfile = xlrd.open_workbook(path)
table = getfile.sheet_by_index(0)
rows = table.nrows

db = pymysql.connect(host='localhost',
        user='root',
        password='zsjnb',
        port=3306,
        charset = 'utf8',
        db='dmtry')
cursor = db.cursor()

def cutdata(data, length, string):
    if string == '':
        return data
    if len(string) < length:
        data.append(string)
        return data
    data.append(string[0:length - 1])
    string = string[length: len(string)]
    return cutdata(data, length, string)

a = {}
for i in range(rows):
    a['old_id'] = table.cell_value(i, 0)
    a['arti_name'] = table.cell_value(i, 1)
    a['kind'] = table.cell_value(i, 3) #文献类型
    a['j_a_name'] = "专利公开号 , "+table.cell_value(i, 19) + ", 专利申请号 ," + table.cell_value(i, 21)
    a['author_name'] = table.cell_value(i, 5)
    a['year'] = table.cell_value(i, 13)
    a['num_view'] = table.cell_value(i, 25)
    a['brief'] = table.cell_value(i, 29)
    name = a['author_name'].split(';')
    a['author_name'] = []
    author_name = ''
    for i in name:
        if i != '':
            i = i.split('[')[0]
            a['author_name'].append(i)
            author_name += (i + ';')                   #数组信息
    author_name = author_name[0:len(author_name) - 1]  #字符串信息
    #print(a)
    
    length = len(a['brief'])
    data = []
    data = cutdata(data, 80, a['brief'])#得到brief的分段信息。
    for j in range(len(data)): 
        data[j] = data[j].replace("\"", "\\\"")
    if (a['arti_name'] == ''):
        continue
    sql = 'select * from achievement_tab where get_id = "%s"'%a['old_id']
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        sql = 'INSERT INTO achievement_tab(name, year, author_name, citation, j_a_name, kind,\
 num_view, get_id, file, link, keyword, brief)VALUES("%s", %d, "%s", -1, "%s", "%s", "%d", "%d", "null",\
 "null", "null", -1)'%(a['arti_name'], a['year'], author_name, a['j_a_name'], a['kind'], a['num_view'], a['old_id'])
        cursor.execute(sql)
        db.commit()
        sql = 'select * from achievement_tab where get_id = "%s"'%a['old_id']
        cursor.execute(sql)
        results = cursor.fetchall()
        a_id = results[0][0]
        #print(a_id)
        print('----------------------------')
        print(data)
        print('----------------------------')
        if len(data) != 0:
            for j in range(len(data)):
                sql = 'INSERT INTO achievement_brief_tab(a_id, brief, number, next_id)VALUES(%d, "%s", %d, 0)' %(a_id, data[j], j)
                print(a['arti_name'])
                print(sql)
                print('-----------------------------------')
                cursor.execute(sql)
                db.commit()
        
        
cursor.close()
db.close()




