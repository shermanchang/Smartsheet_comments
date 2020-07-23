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


def get_TM_work_list():
    work_list = {}
    TM_sheet = ss.Sheets.get_sheet(SHEET_ID_TM)
    for row in TM_sheet.rows:

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
    active = list(
        WorkList.objects.values('owner').order_by('owner').filter(active=True).annotate(work_count=Count('row_id')))
    inactive = list(
        WorkList.objects.values('owner').order_by('owner').filter(active=False).annotate(work_count=Count('row_id')))

    # add active status in list
    for wc in work_count:
        for ac in active:
            if wc["owner"] == ac["owner"]:
                wc["active"] = ac["work_count"]
    for wc in work_count:
        for inac in inactive:
            if wc["owner"] == inac["owner"]:
                wc["inactive"] = inac["work_count"]

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


# Only call by the crontab each weekend, means DB change will not trigger by Web app.
def check_update():
    data = WorkList.objects.all().values()
    db_data = list(data)
    local_work_list = get_TM_work_list()


    # loop the db data, this will only update what already in the db. but no action for new assigning job
    for item in db_data:
        for name, value_list in local_work_list.items():
            if item["owner"] == name:
                for values in value_list:
                    if item["bug"] is not None and item["bug"] == values["bug"]:
                        bug = values["bug"]
                        ss_progress = values["progress"]
                        db_progress = item["progress"]
                        # 清洗数据
                        if ss_progress is None:
                            ss_progress = ""
                        if db_progress is None:
                            db_progress = ""
                        if ss_progress != db_progress:
                            # calculate progress delta & hours change
                            delta_progress = int(ss_progress.replace("%","")) - int(db_progress.replace("%",""))
                            hours_delta = int(values["hours"]) - int(item["hours"] if item["hours"] is not None else "0")
                            print(item["owner"] + item["bug"] + "progress change:" + str(delta_progress)+"%")

                            # 1st, update worklist progress
                            WorkList.objects.filter(bug=item["bug"]).update(
                                progress=ss_progress,
                                progress_delta=str(delta_progress)+"%",
                                hours=str(values["hours"]),
                                hours_delta=str(hours_delta),
                                active=True
                            )
                            # 2nd, update the active status of owner to True
                            Owner.objects.filter(owner=item["owner"]).update(
                                active=True
                            )



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


