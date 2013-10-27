from django.conf.urls import patterns, url

from deleter import views

urlpatterns = patterns('',
    url(r'nuking_account/?$', views.nuking_account, name='nuke'),
    url(r'^$', views.index, name='index')
)
