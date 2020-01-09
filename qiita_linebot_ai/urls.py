from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='callback'),
    path('oauth/', views.oauth, name='oauth'),
]
