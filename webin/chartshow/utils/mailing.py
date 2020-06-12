#!/usr/bin/env python
# encoding: utf-8
"""
@license: Copyright (c) by Ion Beam Applications S.A.
@file: mailing.py
@time: 6/10/2020 11:56 AM
@author: xwchang
"""

# 引入发送邮件的模块
from django.conf import settings
from .weekly_check import get_TM_list, get_TL_list
from django.template import Context, loader
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import collections


def mailing():
    EMAIL_TITLE = 'T30-GZ Performance Tracker'
    FROM_EMAIL = settings.EMAIL_HOST_USER
    TO_ADDRESS = 'xwchang@iba-group.com'
    tm_list = get_TM_list()
    tl_list = get_TL_list()
    tml = list()
    tll = list()
    for i in tm_list:
        tml.append(i['name'])
    dic_tm = collections.Counter(tml)
    for i in tl_list:
        tll.append(i['name'])
    dic_tl = collections.Counter(tll)
    context_tml = {}
    context_tll = {}
    for key in dic_tm:
        context_tml[key] = dic_tm[key]
    for key in dic_tl:
        context_tll[key] = dic_tl[key]
    # 发送的html模板的名称
    email_template_name = 'chartshow/email.html'
    t = loader.get_template(email_template_name)
    html_content = render_to_string('chartshow/email.html', {'context_tml': context_tml, 'context_tll': context_tll})
    msg = EmailMultiAlternatives(EMAIL_TITLE, html_content, FROM_EMAIL, [TO_ADDRESS])
    if msg.get_connection() is not None:
        msg.attach_alternative(html_content, "text/html")
        status = msg.send()
    else:
        status = "No connection to mail server"



