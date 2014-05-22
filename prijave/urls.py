from django.conf.urls import patterns, include, url
from django.views.generic import ListView, CreateView

from prijave.models import Poziv
from prijave import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'volonteri.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.gateway, name = 'gateway'),
    #url(r'^$', ListView.as_view(
                #model = Poziv,
                #template_name = 'prijave_list.html',
                #context_object_name = 'pozivi')),

    url(r'^dolazim/(?P<pk>\d+)$', views.dolazim),
    url(r'^ne-dolazim/(?P<pk>\d+)$', views.ne_dolazim),

    url(r'^nova$', views.PozivCreateView.as_view()),
    url(r'^obustavi/(?P<pk>\d+)$', views.PozivDeleteView.as_view()),
)
