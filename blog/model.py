# -*- coding: UTF-8 -*-
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_all_names():
        categories = list()
        for ac in Category.objects.all():
            categories.append(ac.name)
        return categories


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_all_names():
        labels = list()
        for al in Tag.objects.all():
            labels.append(al.name)
        return labels


class Article(models.Model):
    title = models.CharField(max_length=64, unique=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    abstract = models.TextField(max_length=64 * 1024, unique=False)
    body = models.TextField(max_length=1024 * 1024, unique=False)
    category = models.ForeignKey(Category, unique=False)
    tag = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return self.title


def remove_all():
    Tag.all().delete()
    Category.all().delete()
    Article.all().delete()


def init():
    remove_all()

    for i in range(0, 10):
        al = Tag(name='tag' + str(i))
        al.save()
    for i in range(0, 10):
        ac = Category(name='category' + str(i))
        ac.save()
    for i in range(0, 34):
        __new_article(i).save()


def __new_article(i):
    import random

    ac = Category.objects.get(name='category' + str(random.randint(0, 9)))
    al = Tag.objects.all()[0:random.randint(1, 10)]
    a = Article(title='article' + str(i), abstract='abc' + str(i), body='abc' + str(i), category=ac)
    a.save()
    a.label.add(*al)
    return a
