#!/usr/bin/env python
# encoding: utf-8
"""
@license: Copyright (c) by Ion Beam Applications S.A.
@file: weekly_check.py
@time: 6/9/2020 5:46 PM
@author: xwchang
"""
import smartsheet
import datetime

access_token = "vwlyghxsunr2uzmotowt4wr7ei"

today = datetime.date.today()
week_ago = today - datetime.timedelta(days=7)

# Initialize client
ss = smartsheet.Smartsheet(access_token)
# Make sure we don't miss any error
ss.errors_as_exceptions(True)
action = ss.Sheets.list_sheets(include_all=True)

sheet_map = {}
SHEET_ID_TM = ""
SHEET_ID_TL = ""
for sheet in action.data:
    sheet_map[str(sheet.name)] = str(sheet.id)
    SHEET_ID_TM = sheet_map.get("02 - Guangzhou - Test Matrix")
    SHEET_ID_TL = sheet_map.get("03 - Guangzhou - Task List")
print("got the sheet 'Guangzhou - Test Matrix' id = " + str(SHEET_ID_TM))
print("got the sheet 'Guangzhou - Test Matrix' id = " + str(SHEET_ID_TL))


def get_TM_list():
    response = ss.Discussions.get_all_discussions(
      SHEET_ID_TM,       # sheet_id
      include_all=True)
    discussions = response.data
    employee_list = []
    for row in discussions:
        if row.last_commented_at.date() > week_ago:
            create_date = row.last_commented_at.date().strftime('%Y-%m-%d')
            name = row.created_by.name
            email = row.created_by.email
            id = row.id
            parent_id = row.parent_id
            context = {"id": id, "parent_id": parent_id, "date": create_date, "name": name, "email": email}
            employee_list.append(context)
    return employee_list


def get_TL_list():
    response = ss.Discussions.get_all_discussions(
        SHEET_ID_TL,  # sheet_id
        include_all=True)
    discussions = response.data
    employee_list = []
    for row in discussions:
        if row.last_commented_at.date() > week_ago:
            create_date = row.last_commented_at.date().strftime('%Y-%m-%d')
            name = row.created_by.name
            email = row.created_by.email
            id = row.id
            parent_id = row.parent_id
            context = {"id": id, "parent_id": parent_id, "date": create_date, "name": name, "email": email}
            employee_list.append(context)
    return employee_list





