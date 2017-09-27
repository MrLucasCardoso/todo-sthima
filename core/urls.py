from django.conf.urls import url
from core.views import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^todo/$', TodoList.as_view(), name='todo-list'),
    url(r'^todo/add/$', TodoCreate.as_view(), name='todo-add'),
    url(r'^todo/(?P<pk>[0-9]+)/update/$', TodoUpdate.as_view(), name='todo-update'),
    url(r'^todo/(?P<pk>[0-9]+)/delete/$', TodoDelete.as_view(), name='todo-delete'),
    url(r'^todo/(?P<pk>[0-9]+)/done/$', TodoDone.as_view(), name='todo-done'),
    url(r'^todo/(?P<pk>[0-9]+)/undone/$', TodoUndone.as_view(), name='todo-undone'),
    url(r'^todo/order/$', TodoOrder.as_view(), name='todo-order'),
]
