from django.contrib import admin
from blog.models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_date', 'create_datetime', 'abstract', 'body', 'category')
    search_fields = ('title',)
    list_filter = ('create_datetime', 'category__name', 'label__name')
    filter_horizontal = ('label',)
    fieldsets = (
        (None, {
            'fields': ['title']
        }),
        ('PATH', {
            'fields': ['abstract', 'body']
        }),
        ('CLASSIFY', {
            'fields': ['category', 'label']
        }),
    )


class ArticleInline(admin.TabularInline):
    model = Article


class ArticleLabelInline(admin.TabularInline):
    model = Article.label.through


class ArticleLabelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [ArticleLabelInline]


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [ArticleInline]


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(ArticleLabel, ArticleLabelAdmin)
admin.site.register(Article, ArticleAdmin)