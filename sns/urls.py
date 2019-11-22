from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post, name='post'),
    path('groups', views.groups, name='groups'),
    path('creategroup', views.creategroup, name='creategroup'),
]
