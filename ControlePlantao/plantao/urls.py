from django.urls import path
from . import views

app_name = 'plantao'

urlpatterns = [
    path('<int:list_all>', views.listar, name='listar'),
    path('', views.listar, name='listar'),
    path('calendario/mes/<int:month>/<int:year>/<int:dia_selecionado>', views.calendario_mes, name='calendario'),
    path('novo/', views.CriarPlantao.as_view(), name='criar'),
    path('novo_admin/', views.CriarPlantaoAdmin.as_view(), name='criar_admin'),
    path('resumo/mes/<int:month>/<int:year>', views.resumo_mes, name='resumo'),
    path('meses_anteriores/', views.meses_anteriores, name='meses_anteriores'),
    path('editar/<int:pk>/', views.EditarPlantao.as_view(), name='editar'),
    path('deletar/<int:pk>/', views.DeletarPlantao.as_view(), name='deletar'),
    #path('posts/in/<slug:slug>/', views.SingleGroup.as_view(), name='single'),
    #path('join/<slug:slug>/', views.JoinGroup.as_view(), name='join'),
    #path('leave/<slug:slug>/', views.LeaveGroup.as_view(), name='leave'),
]
