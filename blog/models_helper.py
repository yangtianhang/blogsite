# -*- coding: UTF-8 -*-
from blog.models import Article, Category, Tag

__author__ = 'yangtianhang'


def get_article(article_id):
    return Article.objects.get(id=article_id)


def get_category():
    return Category.objects.all()


def get_tag():
    return Tag.objects.all()


def get_article_count_by_tag(tag_name):
    return Tag.objects.get(name=tag_name).article_set.all().count()


def get_tags_name(article):
    return [tag.name for tag in article.tag.all()]