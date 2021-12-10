from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('records', views.records, name='records'),
    path('record/<int:record_id>', views.record, name='record'),
    path('clients', views.clients, name='clients'),
    path('collector/<slug:client_name>', views.collector, name='collector'),
    path('collector/<slug:client_name>/<slug:tag>', views.collector, name='collector'),
]