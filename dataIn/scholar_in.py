import xlrd
import os
import sys
import pymysql

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
        db='dmtry')
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
    #print(a)
    if (a['name'] == ''):
        continue
    scholar_id = 0
    d_id = 0
    sql = 'select * from scholar_tab where name = "%s";' % (a['name'])
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        sql = 'INSERT INTO scholar_tab(Scholar_Number, name,user_id, email, p_title, flag, get_id, school, Has_Info, brief)VALUES("1","%s", -1, "%s", "%s", 0, "%s","BUAA", 0, 0)'%(a['name'], a['email'], a['p_title'], a['old_id'])
        cursor.execute(sql)
        db.commit()
        sql = 'select * from scholar_tab where name = "%s";' % a['name']
        cursor.execute(sql)
        results = cursor.fetchall()
        scholar_id = results[0][1]
    else:
        continue
    if a['department'] == '':
        continue
    sql = 'select * from department_tab where name = "%s";' % a['department']
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        sql = 'INSERT INTO department_tab(name, number, brief)VALUES("%s", -1, "")'%(a['department'])
        cursor.execute(sql)
        db.commit()
        sql = 'select * from department_tab where name = "%s";' %a['department']
        cursor.execute(sql)
        results = cursor.fetchall()
    d_id = results[0][0]

    print("scholar_id = %s, d_id = %s, name = %s" % (scholar_id, d_id, a['name']))
    sql = 'INSERT INTO scholar_department_tab(scholar_id, d_id)VALUES(%d, %d)'%(scholar_id, d_id)
    cursor.execute(sql)
    db.commit()
cursor.close()
db.close()
