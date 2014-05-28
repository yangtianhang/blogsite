# -*- coding: UTF-8 -*-
import os

ARTICLE_DIR = "~/mysite_resouce"
BLOG_SUB_DIR = "blog"
ABSTRACT_SUB_DIR = "abstract"

BLOG_DIR = os.path.join(ARTICLE_DIR, BLOG_SUB_DIR)
ABSTRACT_DIR = os.path.join(ARTICLE_DIR, ABSTRACT_SUB_DIR)

BASE_URL = 'http://127.0.0.1:8080'
SUB_URL_BLOG = 'blog'
SUB_URL_LABEL = 'label'
SUB_URL_CATEGORY = 'category'
SUB_URL_BLOGS = 'blogs'

LABEL_COLOR_SIZE = 10

COLOR_LIST = ['color-0', 'color-1', 'color-2', 'color-3', 'color-4', 'color-5', 'color-6']
COLOR_LEN = len(COLOR_LIST)

PAGINATION_VISIBLE_SIZE = 7
ARTICLES_PER_PAGE = 5