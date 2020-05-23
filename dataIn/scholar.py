import xlrd
import os
import sys
import pymysql

path = 'data/scholar_all.xlsx'

getfile = xlrd.open_workbook(path)
table = getfile.sheet_by_index(0)
rows = table.nrows
cols = table.ncols

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
    a['way'] = table.cell_value(i, 18)   #研究方向
    a['jianjie'] = table.cell_value(i, 19)  #简介
    a['brief'] = ''
    a['name'] = table.cell_value(i, 2)
    flag = 0
    if len(a['way']) >= 1:
        a['brief'] += ('研究方向:' + a['way'])
        flag = 1
    a['jianjie'] = str(a['jianjie'])
    if (len(a['jianjie']) >= 5):
        a['brief'] += ('\n' + str(a['jianjie']))
        flag = 1
    if flag == 0:
        continue
    sql = 'select * from scholar_tab where get_id = %d;' % (a['old_id']) 
    cursor.execute(sql)
    results = cursor.fetchall()
    if(len(results) == 0):
        continue
    scholar_id = results[0][1]
    print(scholar_id)
    print(a['brief'])#得到学者id和学者简介
    if (a['name'] == ''):
        continue
    data = []
    data = cutdata(data, 80, a['brief'])
    for i in range(len(data)):
        data[i] = data[i].replace('\n', '')
        data[i] = data[i].replace('\"', '\\\"')
        sql = 'insert into scholar_brief_intro_tab(scholar_id, brief, number, next_id)VALUES(%d, "%s", %d, 0)' %(scholar_id, data[i], i)
        cursor.execute(sql)
        db.commit()
cursor.close()
db.close()
