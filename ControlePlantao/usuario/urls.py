from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuario'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='Usuario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastrar/', views.SignUp.as_view(), name='cadastrar'),
    path('editar/<int:pk>/', views.EditarUsuario, name='editar'),
    #path('editar/<int:pk>/', views.EditarUsuario.as_view(), name='editar'),
    path('listar/', views.ListUsers.as_view(), name='listar'),
    path('status/', views.UserStatus.as_view(), name='status'),
    path('mudar_coordenacao_status/<int:coord_status>/<int:usuario>', views.mudar_coordenacao_status, name='mudar_coordenacao_status'),
    path('mudar_ativo_status/<int:ativo_status>/<int:usuario>', views.mudar_ativo_status, name='mudar_ativo_status'),
    path('', auth_views.LoginView.as_view(template_name='Usuario/login.html'), name='login'),
]