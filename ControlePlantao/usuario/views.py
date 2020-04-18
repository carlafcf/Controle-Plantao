from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from . import forms
from .models import User

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('plantao:listar')
    template_name = 'Usuario/cadastrar.html'

class ListUsers(ListView):
    model = User

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

class UserStatus(ListView):
    model = User
    template_name = 'Usuario/status.html'

#class EditarUsuario(UpdateView):
#    model = User
#    form_class = forms.UserUpdateForm
#    success_url = reverse_lazy('plantao:listar')
#    template_name = 'Usuario/user_update_form.html'

def EditarUsuario(request, pk):
    user = User.objects.get(pk = pk)
    # form = ProfileForm(user.values().first())
    form = forms.EditarUsuarioForm(request.POST or None, instance=user)
    if request.method == 'POST':
        #form = forms.EditarUsuarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save(commit=True)
            return redirect('plantao:listar')
    #form = forms.EditarUsuarioForm(user.values().first())
    # print(user)
    context = {
    'form': form
    }
    return render(request, 'Usuario/user_update_form.html',context)

def mudar_coordenacao_status(request, coord_status, usuario):
    user = User.objects.get(pk=usuario)
    if (coord_status==1):
        user.is_superuser = True
    else:
        user.is_superuser = False
    user.save()
    return redirect('usuario:status')

def mudar_ativo_status(request, ativo_status, usuario):
    user = User.objects.get(pk=usuario)
    if (ativo_status==1):
        user.is_active = True
    else:
        user.is_active = False
    user.save()
    return redirect('usuario:status')
