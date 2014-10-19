# -*- coding: UTF-8 -*-

__author__ = 'yangtianhang'


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return "Hello World"