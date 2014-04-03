# -*- coding: UTF-8 -*-

import random

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render

from models import Article
from models import ArticleCategory
from models import ArticleLabel
from mysite.commons import utils
from mysite.commons import constants
from blog.forms import *


__sub_blog = '/' + constants.SUB_URL_BLOG + '/'
__sub_label = '/' + constants.SUB_URL_LABEL + '/'
__sub_category = '/' + constants.SUB_URL_CATEGORY + '/'
__sub_blogs = '/' + constants.SUB_URL_BLOGS + '/'
__sub_blogs_page = '/' + constants.SUB_URL_BLOGS + '/' + 'page' + '/'

__blog_url = constants.BASE_URL + '/' + constants.SUB_URL_BLOG + '/'
__label_url = constants.BASE_URL + '/' + constants.SUB_URL_LABEL + '/'
__category_url = constants.BASE_URL + '/' + constants.SUB_URL_CATEGORY + '/'
__blogs_url = constants.BASE_URL + '/' + constants.SUB_URL_BLOGS + '/'

__len_sub_blogs_url = len(__sub_blog)
__len_sub_label_url = len(__sub_label)
__len_sub_category_url = len(__sub_category)
__len_sub_blogs_url = len(__sub_blogs)
__len_sub_blogs_page = len(__sub_blogs_page)


def index(request):
    # if REFACTORY models decomment belows
    # import models
    # models.init()
    return __blogs(1)


def blogs(request):
    return __blogs(__get_page_num(request))


def edit(request):
    if request.method == 'POST':
        form = EditorForm(request.POST)
        if form.is_valid():
            print 'in request.method'
            print form.cleaned_data['content']
        else:
            print "not valid"
        return 'yeah'
    else:
        return render(request, 'editor.html', {'form': EditorForm()})


def __blogs(page_num):
    count = Article.objects.all().count()
    articles = __get_articles(__get_objects_slide(Article.objects, page_num))
    pagination = __get_pagination(count, page_num, __blogs_url)
    return __response_blogs(articles, pagination)


def label_page(request):
    sub_labels = request.path[__len_sub_label_url:].split('/')
    label_name = sub_labels[0]
    page_num = int(sub_labels[2])
    return __label(label_name, page_num)


def label(request):
    label_name = request.path[__len_sub_label_url:]
    page_num = 1
    return __label(label_name, page_num)


def category(request):
    category_name = request.path[__len_sub_category_url:]
    page_num = 1
    return __category(category_name, page_num)


def category_page(request):
    sub_categories = request.path[__len_sub_category_url:].split('/')
    category_name = sub_categories[0]
    page_num = int(sub_categories[2])
    return __category(category_name, page_num)


def __category(category_name, page_num):
    count = ArticleCategory.objects.get(name=category_name).article_set.all().count()
    articles = __get_articles(
        __get_objects_slide(ArticleCategory.objects.get(name=category_name).article_set.all(), page_num))
    pagination = __get_pagination(count, page_num, __category_url + category_name + '/')
    return __response_blogs(articles, pagination)


def __label(label_name, page_num):
    count = ArticleLabel.objects.get(name=label_name).article_set.all().count()
    articles = __get_articles(
        __get_objects_slide(ArticleLabel.objects.get(name=label_name).article_set.all(), page_num))
    pagination = __get_pagination(count, page_num, __label_url + label_name + '/')
    return __response_blogs(articles, pagination)


def __get_objects_slide(objects, page_num):
    return objects.order_by('-create_datetime')[
           constants.ARTICLES_PER_PAGE * (page_num - 1): constants.ARTICLES_PER_PAGE * page_num]


def __response_blogs(articles, pagination):
    categories = __get_categories()
    labels = __get_labels()
    return utils.response('blogs.html', categories=categories, articles=articles, pagination=pagination,
                          labels=labels)


def blog(request):
    blog_id = __get_blog_id_from_request(request)
    article_object = Article.objects.get(id=blog_id)
    if not article_object:
        return HttpResponse(request.path)
    else:
        article = __get_blog_article(article_object)
        categories = __get_categories()
        labels = __get_labels()
        return utils.response('blog.html', article=article, categories=categories, labels=labels)


def __response_article_abstracts(articles):
    article_abstracts = __get_articles(articles)
    categories = __get_categories()
    t = get_template('index.html')
    html = t.render(Context({'article_list': article_abstracts, 'categories': categories}))
    return HttpResponse(html)


def __get_article_body(article):
    article_body = dict()
    article_body['title'] = article.title
    article_body['body'] = utils.load_abstract(article.body)
    article_body['date'] = utils.get_date_string(article.create_date)
    article_body['category'] = article.category.name
    return article_body


def __get_articles(articles):
    article_abstracts = list()
    for article in articles:
        article_abstracts.append(__get_abstract_article(article))
    return article_abstracts


def __get_abstract_article(article_object):
    article = __get_article(article_object)
    article['abstract'] = utils.load_abstract(article_object.abstract)
    article['read_more'] = __blog_url + str(article_object.id)
    return article


def __get_blog_article(article_object):
    article = __get_article(article_object)
    article['blog'] = utils.load_blog(article_object.abstract)
    return article


def __get_article(article_object):
    article = dict()
    article['title'] = article_object.title
    article['date'] = utils.get_date_string(article_object.create_date)
    article['category'] = __get_category(article_object)
    article['labels'] = __get_label(article_object)
    return article


def __get_categories():
    categories = list()
    for ac in ArticleCategory.objects.all():
        count = ArticleCategory.objects.get(name=ac.name).article_set.all().count()
        categories.append({'url': __category_url + ac.name, 'name': ac.name + ' (' + str(count) + ')'})
    return categories


def __get_blog_id_from_request(request):
    return int(request.path[6:])


def __get_labels():
    labels = list()
    for al in ArticleLabel.objects.all():
        count = ArticleLabel.objects.get(name=al.name).article_set.all().count()
        labels.append({'url': __label_url + al.name,
                       'name': al.name + ' (' + str(count) + ')'})
    return labels


def __get_label(article):
    article_labels = article.label.all()
    color_list = constants.COLOR_LIST[:]
    random.shuffle(color_list)
    html_labels = list()
    ci = 0
    for article_label in article_labels:
        html_labels.append({'url': __label_url + article_label.name,
                            'name': article_label.name,
                            'color': color_list[ci % constants.COLOR_LEN]})
        ci += 1
    return html_labels


def __get_category(article):
    return {'url': __category_url + article.category.name, 'name': article.category.name}


def __get_pagination(count, start_page, href):
    if count <= 0:
        return {}
    return {'total': (count + constants.ARTICLES_PER_PAGE - 1) / constants.ARTICLES_PER_PAGE,
            'startPage': start_page,
            'visible': constants.PAGINATION_VISIBLE_SIZE,
            'href': href + 'page/{{number}}'}


def __get_page_num(request):
    return int(request.path[__len_sub_blogs_page:])
