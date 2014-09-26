# -*- coding: UTF-8 -*-

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


__indicator_clazz = {ArticlesIndicator.CATEGORY: Category,
                     ArticlesIndicator.TAG: Tag,
                     ArticlesIndicator.NONE: None}

__indicator_url = {ArticlesIndicator.CATEGORY: const.BASE_URL + '/' + const.SUB_URL_CATEGORY + '/',
                   ArticlesIndicator.TAG: const.BASE_URL + '/' + const.SUB_URL_LABEL + '/',
                   ArticlesIndicator.NONE: const.BASE_URL + '/' + const.SUB_URL_BLOGS + '/'}


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
        print '=============='
        print tags
        return utils.response('article.html', article=article_body_tpl_obj, categories=categories, labels=tags)


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
                article_id = save_blog(abstract=form.cleaned_data['abstract'],
                                       body=form.cleaned_data['body'],
                                       tag_names=form.cleaned_data['taggit'],
                                       title=form.cleaned_data['subject'],
                                       category_name=form.cleaned_data['selectit'])
                return HttpResponseRedirect(str(article_id))
            else:
                return HttpResponseRedirect(urls.ROOT)
    else:
        if not request.user.is_authenticated():
            return HttpResponseRedirect(urls.LOGIN_URL+'?next=/editor')
        else:
            return render(request, 'editor.html', {'form': EditorForm()})


def update(request):
    pass


def test(request):
    return utils.response('test.html')


def __get_objects_slide(objects, page_num):
    return objects.order_by('-create_datetime')[const.ARTICLES_PER_PAGE * (page_num - 1): const.ARTICLES_PER_PAGE * page_num]


def __response_blogs(articles, pagination):
    categories = __get_categories()
    tags = __get_tags()
    return utils.response('articles.html', categories=categories, articles=articles, pagination=pagination,
                          labels=tags)


def __get_articles(articles):
    article_abstracts = list()
    for article in articles:
        article_abstracts.append(template_helper.get_article_abstract_tpl_obj(article))
    return article_abstracts


def __get_categories():
    category_objs = model_helper.get_category_objs()
    return template_helper.get_categories_tpl_obj(category_objs)


def __get_blog_id_from_request(request):
    return int(request.path[6:])


def __get_tags():
    tag_objs = model_helper.get_tag_objs()
    return template_helper.get_tags(tag_objs, model_helper.get_article_count)


def __get_pagination(count, start_page, href):
    if count <= 0:
        return {}
    return {'total': (count + const.ARTICLES_PER_PAGE - 1) / const.ARTICLES_PER_PAGE,
            'startPage': start_page,
            'visible': const.PAGINATION_VISIBLE_SIZE,
            'href': href + 'page/{{number}}'}
