# -*- coding: UTF-8 -*-
from django import forms
from tinymce.widgets import TinyMCE
from blog.widgets import Taggit
from blog.widgets import ULField
from blog.widgets import DivField
from blog.widgets import Selectit
from models import ArticleLabel, ArticleCategory


class EditorForm(forms.Form):
    subject = forms.CharField(max_length=100)
    taggit = ULField(required=False, widget=Taggit(available_tags=ArticleLabel.get_all_names()))
    selectit = DivField(required=False, widget=Selectit(primitive_options=ArticleCategory.get_all_names()))
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 40}), label='')
