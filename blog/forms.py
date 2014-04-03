# -*- coding: UTF-8 -*-
from django import forms
from tinymce.widgets import TinyMCE


class EditorForm(forms.Form):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 40}), label='')