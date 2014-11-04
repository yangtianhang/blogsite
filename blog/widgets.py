# -*- coding: UTF-8 -*-

import os

from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
from django.forms import Field

JS_URL1 = os.path.join(settings.STATIC_URL, 'taggit/js/tag-it.js')
# JS_URL2 = "http://cdn.bootcss.com/jquery/1.10.2/jquery.min.js"
# JS_URL3 = "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/jquery-ui.min.js"


class ULField(Field):
    def __init__(self, required=True, widget=None, label=None, initial=None, help_text=''):
        super(ULField, self).__init__(required=required, widget=widget, label=label, initial=initial,
                                      help_text=help_text)

    def clean(self, value):
        return value


class DivField(Field):
    def __init__(self, required=True, widget=None, label=None, initial=None, help_text=''):
        super(DivField, self).__init__(required=required, widget=widget, label=label, initial=initial,
                                       help_text=help_text)

    def clean(self, value):
        return value


class Taggit(forms.RadioSelect):
    def __init__(self, attrs=None):
        super(Taggit, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        s1 = '''
        <script type="text/javascript" charset="utf-8">
            $(document).ready(function() {
                $("#tag").tagit({
                fieldName: "tags",
                singleField: true,
                autocomplete: {delay: 0, minLength: 1},
                availableTags: %s
                });
            });
        </script>
        ''' % Taggit._get_available_tags(value['available_tags'])

        s2 = '''
        <ul id="tag" name="tag">
            %s
        </ul>
        ''' % Taggit._get_current_tags(value['current_tags'])

        html = [s1, s2]
        return mark_safe('\n'.join(html))

    @property
    def media(self):
        return forms.Media()

    @staticmethod
    def _get_available_tags(available_tags):
        print available_tags
        return '[%s]' % ','.join(map(lambda x: '"%s"' % x, available_tags))

    @staticmethod
    def _get_current_tags(current_tags):
        print current_tags
        return ''.join(['<li>%s</li>' % current_tag for current_tag in current_tags])

