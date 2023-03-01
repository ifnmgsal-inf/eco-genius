from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from lifetable.models import User

UserModel = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            # 'username',
            'email',
            'password1',
            'password2',
        ]

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            # 'username': 'Nome de usuário',
            'email': 'Email',
            'password1': 'Senha',
            'password2': 'Confirmar senha',
        }

        help_texts = {
            'username': '',
        }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.username = user.email
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user
