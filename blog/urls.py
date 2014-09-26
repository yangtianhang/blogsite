# -*- coding: UTF-8 -*-

__author__ = 'yangtianhang'


from django.conf.urls import patterns, include, url
from enumeration import ArticlesIndicator


urlpatterns = patterns('blog.views',
                       (r'^$', 'get_articles', {'indicator': ArticlesIndicator.NONE}),
                       (r'^all/page/(?P<page>\d+)/*$', 'get_articles', {'indicator': ArticlesIndicator.NONE}),  # /all/page/123

                       (r'^category/(?P<name>[^/]+)/*$', 'get_articles', {'indicator': ArticlesIndicator.CATEGORY}),  # /category/it技术
                       (r'^category/(?P<name>[^/]+)/page/(?P<page>\d*)$', 'get_articles', {'indicator': ArticlesIndicator.CATEGORY}),  # /category/it技术/page/1/

                       (r'^tag/(?P<name>[^/]+)/*$', 'get_articles', {'indicator': ArticlesIndicator.TAG}),  # /tag/leetcode/
                       (r'^tag/(?P<name>[^/]+)/page/(?P<page>\d+)/*$', 'get_articles', {'indicator': ArticlesIndicator.TAG}),  # /tag/leetcode/page/3/

                       (r'^(?P<article_id>\d+)/*$', 'get_article'),  # /1234/

                       (r'^edit/*$', 'edit'),  # /edit
                       (r'^edit/(?P<article_id>\d+)/*$', 'edit'),  # /edit/12

                       # (r'^test', 'test'),
                       )
