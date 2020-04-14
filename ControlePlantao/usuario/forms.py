from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from usuario.models import User

class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nome'
        self.fields['last_name'].label = 'Sobrenome'
        self.fields['username'].label = 'Nome de usuário'
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmar senha'
