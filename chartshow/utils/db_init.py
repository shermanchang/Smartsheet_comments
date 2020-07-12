#!/usr/bin/env python
# encoding: utf-8
"""
@license: Copyright (c) by Ion Beam Applications S.A.
@file: db_init.py
@time: 2020/7/7 14:56
@author: xwchang
"""

# from .weekly_check import get_TM_work_list
# from ..models import Owner, WorkList
#
# # One time call for DB initialize
# print("I am in the DB initial method, "
#       "will do it only once. please comments everthing in the file after 1st run it.")
#
#
# db_owner = Owner.objects.all()
# db_worklist = WorkList.objects.all()
#
# work_list = get_TM_work_list()
#
# for name, data in work_list.items():
#     for item in data:
#         WorkList(row_id=item["row_id"],
#                  owner=name,
#                  mid=item["mid"],
#                  bug=item["bug"],
#                  procedure=item["procedure"],
#                  room=item["room"],
#                  status=item["status"],
#                  progress=item["progress"],
#                  hours=item["hours"],
#                  progress_delta="none",
#                  hours_delta="none",
#                  modified_at=item["modified_at"]).save()







