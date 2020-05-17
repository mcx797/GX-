import xlrd
import os
import sys

path = 'scholar_all.xlsx'

getfile = xlrd.open_workbook('scholar_all.xlsx')
table = getfile.sheet_by_index(0)
rows = table.nrows
cols = table.ncols
#for i in range(rows):
for j in range(cols):
    cell_values = table.cell_value(1, j)
    print(cell_values)
