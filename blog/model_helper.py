# -*- coding: UTF-8 -*-
from blog.model import Article, Category, Tag

__author__ = 'yangtianhang'


def get_article_obj(article_id):
    return Article.objects.get(id=article_id)


def get_category_objs():
    return Category.objects.all()


def get_tag_objs():
    return Tag.objects.all()


def get_article_count(name):
    return Tag.objects.get(name=name).article_set.all().count()

