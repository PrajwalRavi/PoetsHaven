from django.conf.urls import url

from . import views

app_name = 'search'
urlpatterns = [
    # /search
    url(r'^$', views.index, name='index'),

    # /search/query/<query>
    url(r'^query/[a-zA-Z0-9]+/$', views.search, name='search'),

    # /search/display/<id>
    url(r'^display/(?P<file_id>[0-9]+)/$', views.display_file, name='display'),

    # /search/recreate
    # used to update database with file_id, poet, poem name
    url(r'^recreate/$', views.refresh, name='refresh')
]
