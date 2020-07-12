from django.conf import settings
from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string

from .utils import mailing, db_init, weekly_check as wk
from django.template import Context, loader
from django.core.mail import EmailMultiAlternatives
import collections


def index(request):
    # tm_row = wk.get_TM_work_list()
    # # tm_list = wk.get_TM_list()
    # tml = list()
    # for i in tm_list:
    #     tml.append(i['name'])
    # dic_tm = collections.Counter(tml)
    # context_tml = {}
    # listq = []
    # for key in dic_tm:
    #     context_tml[key] = dic_tm[key]
    #     listq.append({'name': key, 'data': [context_tml[key]]})

    work_count, work_list = wk.get_db()
    return render(request, 'chartshow/index.html', {'work_count': work_count,
                                                    'work_list': work_list})


def table(request):
    tm_list = wk.get_TM_list()
    tl_list = wk.get_TL_list()
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

    return render(request, 'chartshow/email.html', {'context_tml': context_tml, 'context_tll': context_tll, 'control': 'yes'})


def send_info(request):
    EMAIL_TITLE = 'T30-GZ Performance Tracker'
    FROM_EMAIL = settings.EMAIL_HOST_USER
    TO_ADDRESS = 'xwchang@iba-group.com'
    tm_list = wk.get_TM_list()
    tl_list = wk.get_TL_list()
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
        return HttpResponse('Email sent manually successfully, with ' + str(status) + ' letter(s)')
    else:
        status = "No connection to mail server"
        return HttpResponse(str(status))


