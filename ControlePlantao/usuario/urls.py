from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuario'

urlpatterns = [
    url('login/', auth_views.LoginView.as_view(template_name='Usuario/login.html'), name='login'),
    url('logout/', auth_views.LogoutView.as_view(), name='logout'),
    url('cadastrar/', views.SignUp.as_view(), name='cadastrar'),
    url('listar/', views.ListUsers.as_view(), name='listar'),
    url('', auth_views.LoginView.as_view(template_name='Usuario/login.html'), name='login'),
]