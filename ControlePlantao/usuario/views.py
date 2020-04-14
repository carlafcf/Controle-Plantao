from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from . import forms
from .models import User

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('usuario:login')
    template_name = 'Usuario/cadastrar.html'

class ListUsers(ListView):
    model = User