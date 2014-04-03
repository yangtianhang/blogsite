from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from mysite import settings


admin.autodiscover()

urlpatterns = patterns('blog.views',
                       (r'^$', 'index'),
                       (r'^label/[^/]+/page/\d+$', 'label_page'),
                       (r'^label/[^/]+$', 'label'),
                       (r'^category/[^/]+/page/\d+$', 'category_page'),
                       (r'^category/[^/]+$', 'category'),
                       (r'^blog/\d+$', 'blog'),
                       (r'^blogs/page/\d+$', 'blogs'),
                       (r'^editor$', 'edit'),
)

urlpatterns += patterns('',
                        url(r'^admin/', include(admin.site.urls)),
                        url(r'^tinymce/', include('tinymce.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

