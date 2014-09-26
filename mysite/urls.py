from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

from mysite import settings


admin.autodiscover()

LOGIN_URL = '/accounts/login/'
ROOT = '/'

urlpatterns = patterns('',
                       url(r'', include('blog.urls')),
)

urlpatterns += patterns('',
                        url(r'^admin/', include(admin.site.urls)),
                        url(r'^tinymce/', include('tinymce.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('',
                        (r'^accounts/login/$', login),
                        (r'^accounts/logout/$', logout),
)

urlpatterns += patterns('',
                        url(r'^ueditor/', include('DjangoUeditor.urls')),
)



