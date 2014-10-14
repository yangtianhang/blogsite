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
    article_object = model_helper.get_article(article_id)

    if not article_object:
        return HttpResponse(request.path)
    else:
        article_body_tpl_obj = template_helper.get_article_body_tpl_obj(article_object)
        categories = __get_categories()
        tags = __get_tags()
        return utils.response('article.html', article=article_body_tpl_obj, categories=categories, labels=tags)


def edit(request, article_id=None):
    if request.method == 'POST':
        return __create_or_update_article(request, article_id)
    else:
        return __get_editor(request, article_id)


def __create_or_update_article(request, article_id):
    if not request.user.is_authenticated():
        return __redirect_login()
    else:
        form = __get_check_article_form(request.POST)

        if form.is_valid():
            article_id = __save_blog(
                abstract=form.cleaned_data['abstract'],
                body=form.cleaned_data['body'],
                tag_names=form.cleaned_data['tags'],
                title=form.cleaned_data['title'],
                category_id=form.cleaned_data['category'],
                article_id=article_id
            )

            return HttpResponseRedirect(urls.ROOT + str(article_id))
        else:
            return HttpResponseRedirect(urls.ROOT)


def __get_editor(request, article_id):
    if not request.user.is_authenticated():
        return __redirect_login()
    else:
        if article_id is None:
            return render(request, 'editor.html', {'form': __get_create_article_form()})
        else:
            return render(request, 'editor.html', {'form': __get_update_article_form(article_id)})


def __redirect_login():
    return HttpResponseRedirect(urls.LOGIN_URL + '?next=/edit')


def __save_blog(title, abstract, body, category_id, tag_names, article_id=None):
    tags = []
    for tag_name in tag_names.split(','):
        tag, is_create = Tag.objects.get_or_create(name=tag_name)
        tags.append(tag)
    category = Category.objects.filter(id=category_id)[0]
    if article_id is None:
        article = Article(title=title, abstract=abstract, body=body, category=category)
    else:
        article = Article.objects.filter(id=article_id)[0]
        article.title = title
        article.abstract = abstract
        article.body = body
        article.category = category

    article.save()
    article.tag.filter().delete()
    article.tag.add(*tags)

    return article.id


def __get_create_article_form():
    editor_form = EditorForm()
    editor_form.fields['category'].choices = __get_category_choices()

    return editor_form


def __get_update_article_form(article_id):
    article = model_helper.get_article(article_id)

    editor_form = EditorForm(initial={
        'title': article.title,
        'body': article.body,
        'abstract': article.abstract,
    })

    editor_form.fields['category'].choices = __get_category_choices()
    editor_form.fields['tags'].widget.extend_available_tags(Tag.get_all_names())
    editor_form.fields['tags'].widget.extend_current_tags(model_helper.get_tags_name(article))

    return editor_form


def __get_check_article_form(post):
    editor_form = EditorForm(post)
    editor_form.fields['category'].choices = __get_category_choices()

    return editor_form


def __get_category_choices():
    return [(str(category.id), category.name) for category in Category.objects.all()]


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
    category_objs = model_helper.get_category()
    return template_helper.get_categories_tpl_obj(category_objs)


def __get_blog_id_from_request(request):
    return int(request.path[6:])


def __get_tags():
    tag_objs = model_helper.get_tag()
    return template_helper.get_tags(tag_objs, model_helper.get_article_count_by_tag)


def __get_pagination(count, start_page, href):
    if count <= 0:
        return {}
    return {'total': (count + const.ARTICLES_PER_PAGE - 1) / const.ARTICLES_PER_PAGE,
            'startPage': start_page,
            'visible': const.PAGINATION_VISIBLE_SIZE,
            'href': href + 'page/{{number}}'}


def test(request):
    return utils.response('test.html')
