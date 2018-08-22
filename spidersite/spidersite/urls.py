from django.conf.urls import include, url
from django.contrib import admin
from sina.views import login_view,logout_view,register_view
urlpatterns = [
    # Examples:
    # url(r'^$', 'spidersite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sina/', include('sina.urls')),
    url(r'^accounts/login/$', login_view),
    url(r'^accounts/logout/$', logout_view),
    url(r'^register_sina/', register_view),   
]
