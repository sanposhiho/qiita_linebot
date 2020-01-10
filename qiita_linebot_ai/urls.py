from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='callback'),
    path('oauth/line/', views.line_oauth, name='line_oauth'),
    path('oauth/qiita/', views.qiita_oauth, name='qiita_oauth'),
]
