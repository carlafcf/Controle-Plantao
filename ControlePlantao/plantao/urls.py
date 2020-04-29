from django.urls import path
from . import views

app_name = 'plantao'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:list_all>', views.listar, name='listar'),
    path('listar/', views.listar, name='listar'),
    path('plantoes_usuario/<int:pk>', views.plantoes_usuario, name='plantoes_usuario'),
    path('calendario/mes/<int:month>/<int:year>/<int:dia_selecionado>', views.calendario_mes, name='calendario'),
    path('novo/', views.CriarPlantao.as_view(), name='criar'),
    path('novo_admin/', views.CriarPlantaoAdmin.as_view(), name='criar_admin'),
    path('resumo/', views.resumo_mes, name='resumo_mes'),
    path('meses_anteriores/', views.meses_anteriores, name='meses_anteriores'),
    path('meses_anteriores_admin/', views.meses_anteriores_admin, name='meses_anteriores_admin'),
    path('trocar_horas_mes/', views.trocar_horas_mes, name='trocar_horas_mes'),
    path('editar/<int:pk>/', views.EditarPlantao.as_view(), name='editar'),
    path('editar_admin/<int:pk>/', views.EditarPlantaoAdmin.as_view(), name='editar_admin'),
    path('deletar/<int:pk>/', views.DeletarPlantao.as_view(), name='deletar'),
    #path('posts/in/<slug:slug>/', views.SingleGroup.as_view(), name='single'),
    #path('join/<slug:slug>/', views.JoinGroup.as_view(), name='join'),
    #path('leave/<slug:slug>/', views.LeaveGroup.as_view(), name='leave'),
]
