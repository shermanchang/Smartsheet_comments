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
import re

from django.db.models import Count

from ..models import Owner, WorkList

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

# collect all member name:
work_list = {}


def get_TM_work_list():
    TM_sheet = ss.Sheets.get_sheet(SHEET_ID_TM)
    for row in TM_sheet.rows:
        # if str(row.cells[1].display_value).startswith('ML'):
        #     if re.match("^ML[\d]*$", row.cells[1].display_value) is not None:
        #         print(row.cells[1].display_value, row.cells[2].display_value)

        name = row.cells[7].display_value
        status = row.cells[8].display_value
        if status not in ["QA", "Closed", "Admin", "CCB"]:
            if name is not None and name not in work_list:
                work_list[name] = [{"bug": row.cells[6].display_value,
                                    "mid": row.cells[4].display_value,
                                    "procedure": row.cells[2].display_value,
                                    "room": row.cells[1].display_value,
                                    "status": row.cells[8].display_value,
                                    "progress": row.cells[9].display_value,
                                    "hours": row.cells[10].display_value,
                                    "modified_at": row.modified_at.date(),
                                    "row_id": row.id_,
                                    }]
            elif name is not None and name in work_list:
                work_list[name].append({"bug": row.cells[6].display_value,
                                        "mid": row.cells[4].display_value,
                                        "procedure": row.cells[2].display_value,
                                        "room": row.cells[1].display_value,
                                        "status": row.cells[8].display_value,
                                        "progress": row.cells[9].display_value,
                                        "hours": row.cells[10].display_value,
                                        "modified_at": row.modified_at.date(),
                                        "row_id": row.id_,
                                        })
    return work_list


def get_db():
    data = WorkList.objects.all().values()
    db_data = list(data)
    # get all name
    work_count = list(WorkList.objects.values('owner').order_by('owner').annotate(work_count=Count('row_id')))

    list_by_name = []
    # packaging the data
    for item in db_data:
        for li in work_count:
            if item["owner"] is not None and item["owner"] == li["owner"]:
                if item["hours_delta"] == "none":
                    item["hours_delta"] = "0"
                if item["progress_delta"] == "none":
                    item["progress_delta"] = "0"
                list_by_name.append(item)
    return work_count, list_by_name


# Only call by the crontab each week, means DB change will not trigger by Web app.
def check_update():
    data = WorkList.objects.all().values()
    db_data = list(data)
    local_work_list = get_TM_work_list()
    # loop the db data
    for item in db_data:
        for name, value_list in local_work_list.items():
            if item["owner"] == name:
                for values in value_list:
                    if item["bug"] is not None and item["bug"] == values["bug"]:
                        bug = values["bug"]
                        ss_progress = values["progress"]
                        db_progress = item["progress"]
                        if ss_progress is None:
                            ss_progress = ""
                        if db_progress is None:
                            db_progress = ""
                        if ss_progress != db_progress:
                            print('1st update progress')
                            print('2nd update progress_delta')


def get_TM_list():
    response = ss.Discussions.get_all_discussions(
        SHEET_ID_TM,  # sheet_id
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


