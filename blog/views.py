# -*- coding: UTF-8 -*-

import random

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from blog import model_helper
from blog import template_helper
from model import Article
from mysite import urls
from mysite.commons import utils
from blog.forms import *
from enumeration import ArticlesIndicator
from constant import const


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

__indicator_clazz = {ArticlesIndicator.CATEGORY: Category,
                     ArticlesIndicator.TAG: Tag,
                     ArticlesIndicator.NONE: None}

__indicator_url = {ArticlesIndicator.CATEGORY: __category_url,
                   ArticlesIndicator.TAG: __tag_url,
                   ArticlesIndicator.NONE: __blogs_url}


def get_articles(request, indicator=None, page=None, name=None):
    if page is None:
        page = 1
    page = int(page)
    if page < 1:
        page = 1

    clazz = __indicator_clazz[indicator]
    url = __indicator_url[indicator]

    if clazz is None:
        count = Article.objects.all().count()
        articles = __get_articles(__get_objects_slide(Article.objects, page))
        pagination = __get_pagination(count, page, url)
    else:
        count = clazz.objects.get(name=name).article_set.all().count()
        articles = __get_articles(__get_objects_slide(clazz.objects.get(name=name).article_set.all(), page))
        pagination = __get_pagination(count, page, url + name + '/')

    return __response_blogs(articles, pagination)


def get_article(request, article_id):
    article_object = model_helper.get_article_obj(article_id)

    if not article_object:
        return HttpResponse(request.path)
    else:
        article_body_tpl_obj = template_helper.get_article_body_tpl_obj(article_object)
        categories = __get_categories()
        tags = __get_tags()
        return utils.response('blog.html', article=article_body_tpl_obj, categories=categories, labels=tags)


def edit(request):
    def save_blog(title, abstract, body, category_name, tag_names):
        category, is_create = Category.objects.get_or_create(name=category_name)

        tags = []
        for tag_name in tag_names.split(','):
            tag, is_create = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)

        article = Article(title=title, abstract=abstract, body=body, category=category)
        article.save()
        article.tag.add(*tags)

        return article.id

    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseRedirect(urls.LOGIN_URL+'?next=/editor/')
        else:
            form = EditorForm(request.POST)
            if form.is_valid():
                article_id = save_blog(abstract=form.cleaned_data['content'],
                                       body=form.cleaned_data['content'],
                                       tag_names=form.cleaned_data['taggit'],
                                       title=form.cleaned_data['subject'],
                                       category_name=form.cleaned_data['selectit'])
                return HttpResponseRedirect('/blog/' + str(article_id))
            else:
                return HttpResponseRedirect(urls.ROOT)
    else:
        if not request.user.is_authenticated():
            return HttpResponseRedirect(urls.LOGIN_URL+'?next=/editor')
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


def test(request):
    return utils.response('test.html')


def __category(category_name, page_num):
    count = Category.objects.get(name=category_name).article_set.all().count()
    articles = __get_articles(
        __get_objects_slide(Category.objects.get(name=category_name).article_set.all(), page_num))
    pagination = __get_pagination(count, page_num, __category_url + category_name + '/')
    return __response_blogs(articles, pagination)


def __label(label_name, page_num):
    count = Tag.objects.get(name=label_name).article_set.all().count()
    articles = __get_articles(
        __get_objects_slide(Tag.objects.get(name=label_name).article_set.all(), page_num))
    pagination = __get_pagination(count, page_num, __tag_url + label_name + '/')
    return __response_blogs(articles, pagination)


def __get_objects_slide(objects, page_num):
    return objects.order_by('-create_datetime')[const.ARTICLES_PER_PAGE * (page_num - 1): const.ARTICLES_PER_PAGE * page_num]


def __response_blogs(articles, pagination):
    categories = __get_categories()
    labels = __get_tags()
    return utils.response('articles.html', categories=categories, articles=articles, pagination=pagination,
                          labels=labels)

def __response_article_abstracts(articles):
    article_abstracts = __get_articles(articles)
    categories = __get_categories()
    t = get_template('index.html')
    html = t.render(Context({'article_list': article_abstracts, 'categories': categories}))
    return HttpResponse(html)


def __get_articles(articles):
    article_abstracts = list()
    for article in articles:
        article_abstracts.append(template_helper.get_article_abstract_tpl_obj(article))
    return article_abstracts


# def __get_blog_article(article_object):
# article = __get_article(article_object)
# article['blog'] = utils.load_blog(article_object.abstract)
# return article


def __get_article(article_object):
    article = dict()
    article['title'] = article_object.title
    article['date'] = utils.get_date_string(article_object.create_datetime)
    article['category'] = __get_category(article_object)
    article['labels'] = __get_label(article_object)
    return article


def __get_categories():
    category_objs = model_helper.get_category_objs()
    return template_helper.get_categories_tpl_obj(category_objs)


def __get_blog_id_from_request(request):
    return int(request.path[6:])


def __get_tags():
    tag_objs = model_helper.get_tag_objs()
    return template_helper.get_tags(tag_objs, model_helper.get_article_count)


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


def __get_category(article):
    return {'url': __category_url + article.category.name, 'name': article.category.name}


def __get_pagination(count, start_page, href):
    if count <= 0:
        return {}
    return {'total': (count + const.ARTICLES_PER_PAGE - 1) / const.ARTICLES_PER_PAGE,
            'startPage': start_page,
            'visible': const.PAGINATION_VISIBLE_SIZE,
            'href': href + 'page/{{number}}'}


def __get_page_num(request):
    return int(request.path[__len_sub_blogs_page:])
