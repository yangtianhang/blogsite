# -*- coding: UTF-8 -*-
from django import forms
from  DjangoUeditor.widgets import UEditorWidget

from blog.widgets import Taggit
from blog.widgets import ULField
from blog.widgets import DivField
from blog.widgets import Selectit
from model import Tag, Category


class EditorForm(forms.Form):
    title = forms.CharField(max_length=100)
    taggit = ULField(required=False, widget=Taggit(available_tags=Tag.get_all_names()))
    selectit = DivField(required=False, widget=Selectit(primitive_options=Category.get_all_names()))

    body = forms.CharField(label="内容", widget=UEditorWidget({'width': 800, 'height': 600}))
    abstract = forms.CharField(label="摘要", widget=UEditorWidget({'width': 800, 'height': 300}))
