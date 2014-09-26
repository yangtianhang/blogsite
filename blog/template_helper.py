# -*- coding: UTF-8 -*-
import random

from constant import const


__author__ = 'yangtianhang'

# tpl -> template

__sub_blog = '/' + const.SUB_URL_BLOG + '/'
__sub_label = '/' + const.SUB_URL_LABEL + '/'
__sub_category = '/' + const.SUB_URL_CATEGORY + '/'
__sub_blogs = '/' + const.SUB_URL_BLOGS + '/'
__sub_blogs_page = '/' + const.SUB_URL_BLOGS + '/' + 'page' + '/'

__blog_url = const.BASE_URL + '/' + const.SUB_URL_BLOG + '/'
__tag_url = const.BASE_URL + '/' + const.SUB_URL_LABEL + '/'
__category_url = const.BASE_URL + '/' + const.SUB_URL_CATEGORY + '/'
__blogs_url = const.BASE_URL + '/' + const.SUB_URL_BLOGS + '/'

__len_sub_blogs_url = len(__sub_blog)
__len_sub_label_url = len(__sub_label)
__len_sub_category_url = len(__sub_category)
__len_sub_blogs_url = len(__sub_blogs)
__len_sub_blogs_page = len(__sub_blogs_page)


def get_article_body_tpl_obj(article_obj):
    article_template_obj = dict()
    article_template_obj['title'] = article_obj.title
    article_template_obj['blog'] = article_obj.body
    article_template_obj['date'] = __get_date_string(article_obj.create_datetime)
    article_template_obj['category'] = article_obj.category.name

    return article_template_obj


def get_article_abstract_tpl_obj(article_obj):
    article = dict()
    article['title'] = article_obj.title
    article['date'] = __get_date_string(article_obj.create_datetime)
    article['category'] = article_obj.category.name
    article['labels'] = __get_label(article_obj)
    article['abstract'] = article_obj.abstract
    article['read_more'] = str(article_obj.id)
    return article


def get_categories_tpl_obj(category_objs):
    categories_tpl_obj = list()

    for c in category_objs:
        categories_tpl_obj.append({'url': __category_url + c.name, 'name': c.name})

    return categories_tpl_obj


def get_tags(tag_objs, get_count):
    tags_tpl_obj = list()

    for t in tag_objs:
        count = get_count(t.name)
        tags_tpl_obj.append({'url': __tag_url + t.name, 'name': t.name + ' (' + str(count) + ')'})

    return tags_tpl_obj


def __get_date_string(date):
    return '%d 年 %d 月 %d 日' % (date.year, date.month, date.day)


def __get_label(article):
    article_labels = article.tag.all()
    color_list = const.COLOR_LIST[:]
    random.shuffle(color_list)
    html_labels = list()
    ci = 0
    for article_label in article_labels:
        html_labels.append({'url': __tag_url + article_label.name,
                            'name': article_label.name,
                            'color': color_list[ci % const.COLOR_LEN]})
        ci += 1
    return html_labels
