from django.conf.urls import url

from . import views

app_name = 'search'
urlpatterns = [
    # /search
    url(r'^$', views.index, name='index'),

    # /search/<query>
    #url(r'^(?P<query>[a-zA-Z0-9]+)/$', views.search, name='search')
    url(r'^[a-zA-Z0-9]+/$', views.search, name='search')
]
