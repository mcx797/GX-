import xlrd
import os
import sys
import pymysql
import time
from datetime import datetime
from xlrd import xldate_as_tuple

path = 'relation_all.xlsx'

getfile = xlrd.open_workbook(path)
table = getfile.sheet_by_index(0)
rows = table.nrows

db = pymysql.connect(host='localhost',
        user='root',
        password='zsjnb',
        port=3306,
        charset = 'utf8',
        db='dmtrydb')
cursor = db.cursor()

a = {}
for i in range(rows):
    a['scholar_id'] = table.cell_value(i, 0)
    a['a_id'] = table.cell_value(i, 1)
    sql = "select a_id from achievement_tab where get_id = %d" % a['a_id']
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        continue
    a['a_id'] = results[0][0]
    print(results[0][0])
    sql = "select scholar_id from scholar_tab where get_id = %d" % a['scholar_id']
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        continue
    print(results[0][0])
    a['scholar_id'] = results[0][0]
    sql = "select * from scholar_achievement_tab where a_id = %d and scholar_id = %d" %(a['a_id'], a['scholar_id'])
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) != 0:
        print("chongfu")
        continue
    print('----------------------------')
    sql = 'INSERT INTO scholar_achievement_tab(scholar_id, a_id)VALUES("%d", "%d")'%(a['scholar_id'], a['a_id'])
    cursor.execute(sql)
    db.commit()
cursor.close()
db.close()
