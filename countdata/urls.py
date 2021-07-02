from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'countdata'

urlpatterns = [
	path('', views.index, name='index'),
    path('result/', views.result, name='result'),
]