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


class Selectit(forms.Widget):
    def __init__(self, select_name='selectit', primitive_options=None, attrs=None):
        super(Selectit, self).__init__(attrs)
        if primitive_options is None:
            primitive_options = '[]'
        self.available_options_string = self.__init_available_options_string(primitive_options)
        self.select_name = select_name

    def render(self, name, value, attrs=None):
        s1 = '''
        <script type="text/javascript" charset="utf-8">
        $(document).ready(function() {
            $("#selectit").selectit({
                availableSelection: %s,
                select_name: '%s'
            });
        });
        </script>
        ''' % (self.available_options_string, self.select_name)

        print s1

        s2 = '''
        <div id="selectit" name="selectit">
        </div>
        '''
        html = [s1, s2]
        return mark_safe('\n'.join(html))

    def __init_available_options_string(self, primitive_options):
        if primitive_options is None or not primitive_options:
            primitive_options = '[]'
        return '["' + '","'.join(primitive_options) + '"]'

    @property
    def media(self):
        return forms.Media()


class Taggit(forms.RadioSelect):
    def __init__(self, attrs=None, tag_attrs=None, available_tags=None):
        super(Taggit, self).__init__(attrs)
        if tag_attrs is None:
            tag_attrs = {}
        self.tag_attrs = tag_attrs
        if available_tags is None:
            available_tags = []
        self._availableTags = available_tags

    def render(self, name, value, attrs=None):
        s1 = '''
        <script type="text/javascript" charset="utf-8">
            $(document).ready(function() {
                $("#tag").tagit({
                fieldName: "taggit",
                singleField: true,
                autocomplete: {delay: 0, minLength: 1},
                availableTags: %s
                });
            });
        </script>
        ''' % Taggit.__convert_to_list_str(self._availableTags)

        s2 = '''
        <ul id="tag" name="tag">
        </ul>
        '''
        html = [s1, s2]
        return mark_safe('\n'.join(html))

    @property
    def media(self):
        return forms.Media()

    @staticmethod
    def __convert_to_list_str(l):
        return '[%s]' % ','.join(map(lambda x: '"%s"' % x, l))

