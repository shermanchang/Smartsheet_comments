#!/usr/bin/env python
# encoding: utf-8
"""
@license: Copyright (c) by Ion Beam Applications S.A.
@file: db_init.py
@time: 2020/7/7 14:56
@author: xwchang
"""

from .weekly_check import get_TM_work_list
from ..models import Owner, WorkList
from django.db.models import Count

# One time call for DB initialize
# print("I am in the DB initial method, will do it only once. please comments everthing in the file after 1st run it.")
#
#
# db_owner = Owner.objects.all()
# db_worklist = WorkList.objects.all()
# db_worklist = [int(str(i)) for i in db_worklist]
#
# work_list = get_TM_work_list()
#
# # 1st, insert the work list
# for name, data in work_list.items():
#     for item in data:
#         if item["row_id"] not in db_worklist:
#             WorkList(row_id=item["row_id"],
#                      owner=name,
#                      mid=item["mid"],
#                      bug=item["bug"],
#                      procedure=item["procedure"],
#                      room=item["room"],
#                      status=item["status"],
#                      progress=item["progress"],
#                      hours=item["hours"],
#                      progress_delta="none",
#                      hours_delta="none",
#                      modified_at=item["modified_at"],
#                      active=False).save()
#
# # 2nd, after got work list, we group by user, insert the owners
# ownerlist = list(WorkList.objects.values('owner').order_by('owner').annotate(work_count=Count('row_id')))
# for owner in ownerlist:
#     Owner(owner=owner["owner"],
#           active=True).save()





