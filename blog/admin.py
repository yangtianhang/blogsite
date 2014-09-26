from django.contrib import admin
from blog.model import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_datetime', 'abstract', 'body', 'category')
    search_fields = ('title',)
    list_filter = ('create_datetime', 'category__name', 'tag__name')
    filter_horizontal = ('tag',)
    fieldsets = (
        (None, {
            'fields': ['title']
        }),
        ('PATH', {
            'fields': ['abstract', 'body']
        }),
        ('CLASSIFY', {
            'fields': ['category', 'tag']
        }),
    )


class ArticleInline(admin.TabularInline):
    model = Article


class ArticleTagInline(admin.TabularInline):
    model = Article.tag.through


class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [ArticleTagInline]


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [ArticleInline]


admin.site.register(Category, ArticleCategoryAdmin)
admin.site.register(Tag, ArticleTagAdmin)
admin.site.register(Article, ArticleAdmin)