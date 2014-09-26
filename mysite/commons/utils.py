# -*- coding: UTF-8 -*-

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def response(template, **context):
    template = get_template(template)
    html = template.render(Context(context))
    return HttpResponse(html)


def get_date_string(date):
    return '%d 年 %d 月 %d 日' % (date.year, date.month, date.day)

