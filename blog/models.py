# -*- coding: UTF-8 -*-
from django.db import models


class ArticleCategory(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_all_names():
        categories = list()
        for ac in ArticleCategory.objects.all():
            categories.append(ac.name)
        return categories


class ArticleLabel(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_all_names():
        labels = list()
        for al in ArticleLabel.objects.all():
            labels.append(al.name)
        return labels


class Article(models.Model):
    title = models.CharField(max_length=64, unique=True)
    create_date = models.DateField(auto_now_add=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    abstract = models.CharField(max_length=128, unique=True)
    body = models.CharField(max_length=128, unique=True)
    category = models.ForeignKey(ArticleCategory, blank=True, unique=False)
    label = models.ManyToManyField(ArticleLabel, blank=True)

    def __unicode__(self):
        return self.title


def init():
    ArticleLabel.objects.all().delete()
    ArticleCategory.objects.all().delete()
    Article.objects.all().delete()
    for i in range(0, 10):
        al = ArticleLabel(name='label' + str(i))
        al.save()
    for i in range(0, 10):
        ac = ArticleCategory(name='category' + str(i))
        ac.save()
    for i in range(0, 34):
        __new_article(i).save()


def __new_article(i):
    import random

    ac = ArticleCategory.objects.get(name='category' + str(random.randint(0, 9)))
    al = ArticleLabel.objects.all()[0:random.randint(1, 10)]
    a = Article(title='article' + str(i), abstract='abc' + str(i), body='abc' + str(i), category=ac)
    a.save()
    a.label.add(*al)
    return a
