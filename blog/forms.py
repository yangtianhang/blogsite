# -*- coding: UTF-8 -*-
from django import forms
from DjangoUeditor.widgets import UEditorWidget

from blog.widgets import Taggit
from blog.widgets import ULField
from model import Tag, Category


class EditorForm(forms.Form):
    title = forms.CharField(label="题目", max_length=100)
    tags = ULField(label="标签", required=False, widget=Taggit())
    category = forms.ChoiceField(label="分类")
    body = forms.CharField(label="内容", widget=UEditorWidget({'width': 800, 'height': 600}))
    abstract = forms.CharField(label="摘要", widget=UEditorWidget({'width': 800, 'height': 300}))
