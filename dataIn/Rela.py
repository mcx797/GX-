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
    print("%d  %d"%(a['scholar_id'], a['a_id']))
    sql = 'INSERT INTO scholar_achievement_tab(scholar_id, a_id)VALUES("%d", "%d")'%(a['scholar_id'], a['a_id'])
    cursor.execute(sql)
    db.commit()
cursor.close()
db.close()
