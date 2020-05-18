import xlrd
import os
import sys
import pymysql
import time
from datetime import datetime
from xlrd import xldate_as_tuple

path = 'Achievement1.xlsx'

def hasNoData(results, find, i):
    for row in results:
        print(row[i])
        if row[i] == find:
            print(row[i])
            return False
    return True


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
    a['old_id'] = table.cell_value(i, 0)
    a['arti_name'] = table.cell_value(i, 1)
    a['kind'] = table.cell_value(i, 5) #文献类型
    a['j_a_name'] = table.cell_value(i, 11)
    a['year'] = table.cell_value(i, 15)
    date = datetime(*xldate_as_tuple(a['year'], 0))
    a['year'] = date.strftime('%Y')
    a['num_view'] = table.cell_value(i, 19)
    #print(a)
    if (a['arti_name'] == ''):
        continue
    sql = 'select * from achievement_tab'
    cursor.execute(sql)
    results = cursor.fetchall()
    if (hasNoData(results, a['old_id'], 8)):
        sql = 'INSERT INTO achievement_tab(name,\
         year, author_name, citation, j_a_name,\
          kind, num_view, get_id, file, link, keyword)VALUES("%s", "%s", \
          "见关联表",\
           -1, "%s", "%s", "%d", "%d", "null", "null", "null"\
          )'%(a['arti_name'], a['year'], a['j_a_name'], a['kind'], a['num_view'], a['old_id'])
        cursor.execute(sql)
        db.commit()
cursor.close()
db.close()
