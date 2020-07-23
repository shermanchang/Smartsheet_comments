#!/usr/bin/env python
# encoding: utf-8
"""
@license: Copyright (c) by Ion Beam Applications S.A.
@file: flowchart_db.py
@time: 2020/7/23 14:56
@author: xwchang
"""
from .weekly_check import get_TM_work_list
from ..models import Flowchart_mid
from datetime import date
from django.db.models import Count
import xlrd

# One time call for DB initialize
# print("I am in the flowchart DB initial method.")
#
#
# # Read from excel
# def read_xlrd(excelFile):
#     data = xlrd.open_workbook(excelFile)
#     table = data.sheet_by_index(0)
#     dataList = []
#     column_name = table.row_values(0)
#     for rowNum in range(table.nrows):
#         # if 去掉表头
#         if rowNum > 0 and table.row_values(rowNum)[0] != "":
#             dataList.append(table.row_values(rowNum))
#
#     return column_name, dataList
#
#
# excelFile = 'chartshow/static/chartshow/files/STM.xlsx'
# column, data = read_xlrd(excelFile=excelFile)
# print("Start to insert the flowchart table")
#
# # insert the flowchart table
# for row in data:
#     Flowchart_mid(row=row[0],
#                   col=row[1],
#                   background_group=row[2],
#                   room=row[3],
#                   procedure=row[4],
#                   test_type=row[5],
#                   mid=row[6],
#                   ccp=row[7],
#                   bug=row[8],
#                   owner=row[9],
#                   status=row[10],
#                   progress=row[11],
#                   hours=row[12],
#                   progress_delta="",
#                   hours_delta="",
#                   modified_at=date.today(),
#                   active=True).save()
