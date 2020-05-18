import xlrd
import os
import sys
import pymysql



def hasNoData(results, find, i):
    for row in results:
        if row[i] == find:
            print(row[i])
            return False
    return True

def getScholarId(results, find):
    print("in")
    print("find")
    print(find)
    for row in results:
        if row[3] == find:
            print(row[3])
            return row[1]

def getDId(results, find):
    for row in results:
        if row[2] == find:
            return row[0]


path = 'scholar_all.xlsx'

getfile = xlrd.open_workbook('scholar_all.xlsx')
table = getfile.sheet_by_index(0)
rows = table.nrows
cols = table.ncols
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
    a['name'] = table.cell_value(i, 2)
    a['department'] = table.cell_value(i, 6)
    a['p_title'] = table.cell_value(i, 10) #职称
    a['email'] = table.cell_value(i, 14)
    a['phone'] = table.cell_value(i, 16)
    a['way'] = table.cell_value(i, 18)   #研究方向
    a['jianjie'] = table.cell_value(i, 19)  #简介
    print(a)
    if (a['name'] == ''):
        continue
    scholar_id = 0
    d_id = 0
    sql = 'select * from scholar_tab'
    cursor.execute(sql)
    results = cursor.fetchall()
    if (hasNoData(results, a['name'], 3)):
        sql = 'INSERT INTO scholar_tab(Scholar_Number, name, user_id, email, p_title, flag, get_id, school)VALUES("1", "%s", -1, "%s", "%s", 0, "%s", "BUAA")'%(a['name'], a['email'], a['p_title'], a['old_id'])
        cursor.execute(sql)
        db.commit()
        sql = 'select * from scholar_tab'
        cursor.execute(sql)
        results = cursor.fetchall()
        scholar_id = getScholarId(results, a['name'])
    else:
        continue
    sql = 'select * from department_tab;'
    cursor.execute(sql)
    results = cursor.fetchall()
    if (hasNoData(results, a['department'], 2)):
        sql = 'INSERT INTO department_tab(name, number, brief)VALUES("%s", -1, "")'%(a['department'])
        cursor.execute(sql)
        db.commit()
    sql = 'select * from department_tab'
    cursor.execute(sql)
    results = cursor.fetchall()
    d_id = getDId(results, a['department'])
    print("scholar_id = %s, d_id = %s, name = %s" % (scholar_id, d_id, a['name']))
    sql = 'INSERT INTO scholar_department_tab(scholar_id, d_id)VALUES(%d, %d)'%(scholar_id, d_id)
    cursor.execute(sql)
    db.commit()
cursor.close()
db.close()
