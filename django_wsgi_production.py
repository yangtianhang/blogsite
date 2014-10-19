# -*- coding: utf-8 -*-  

__author__ = 'yang'
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings_pro")

from django.core.handlers.wsgi import WSGIHandler

application = WSGIHandler()
