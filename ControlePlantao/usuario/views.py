from django.views.generic import CreateView
from django.urls import reverse_lazy
from . import forms

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('usuario:login')
    template_name = 'Usuario/cadastrar.html'