import xlrd
import os
import sys

path = 'scholar_all.xlsx'

getfile = xlrd.open_workbook('scholar_all.xlsx')
table = getfile.sheet_by_index(0)
rows = table.nrows
cols = table.ncols
for i in range(rows):
#for j in range(cols):
    a = {}
    cell_values = table.cell_value(i, 0)
    a['old_id'] = table.cell_value(i, 0)
    a['name'] = table.cell_value(i, 2)
    a['department'] = table.cell_value(i, 6)
    a['p_title'] = table.cell_value(i, 10) #职称
    a['email'] = table.cell_value(i, 14)
    a['phone'] = table.cell_value(i, 16)
    a['way'] = table.cell_value(i, 18)   #研究方向
    a['jianjie'] = table.cell_value(i, 19)  #简介
    print(a)
