# -*- coding: UTF-8 -*-
import codecs
import os

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from mysite.commons import constants


def response(template, **context):
    template = get_template(template)
    html = template.render(Context(context))
    return HttpResponse(html)


def load_abstract(file_name):
    return load_file(os.path.join(constants.ABSTRACT_DIR, file_name))


def load_blog(file_name):
    return load_file(os.path.join(constants.BLOG_DIR, file_name))


def save_blog_file(file_name, content):
    path = os.path.join(constants.BLOG_DIR, file_name)
    with open(path, 'w') as fp:
        fp.write(content)


def get_date_string(date):
    return '%d 年 %d 月 %d 日' % (date.year, date.month, date.day)


def load_file(path):
    path = path.replace('\\', '/')
    print path
    try:
        with codecs.open(path, 'r', 'utf-8') as f:
            return f.read()
    except Exception, e:
        return __handle_load_file_exception(e, path)


def __handle_load_file_exception(e, path):
    print e
    return None
