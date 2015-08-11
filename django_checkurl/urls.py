from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_checkurl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', 'checkurl.views.urlform', name='urlform'),
    url(r'^report/', 'checkurl.views.report', name='report'),
    url(r'^emailreport/', 'checkurl.views.emailreport', name='emailreport'),
    url(r'^fetchreport/', 'checkurl.views.fetchreport', name='fetchreport'),

)
