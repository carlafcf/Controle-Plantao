from django.urls import path
from . import views

app_name = 'plantao'

urlpatterns = [
    path('', views.listar, name='listar'),
    path('novo/', views.CriarPlantao.as_view(), name='criar'),
    #path('posts/in/<slug:slug>/', views.SingleGroup.as_view(), name='single'),
    #path('join/<slug:slug>/', views.JoinGroup.as_view(), name='join'),
    #path('leave/<slug:slug>/', views.LeaveGroup.as_view(), name='leave'),
]
