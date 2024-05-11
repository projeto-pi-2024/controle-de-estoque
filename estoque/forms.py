from django import forms
from .models import *
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'custo', 'codigo_barras',
                  'preco_venda', 'quantidade_inicial', 'categoria', 'situacao',]


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['movimentacao', 'quantidade']
        labels = {
            'movimentacao': 'Movimentação',
            'quantidade': 'Quantidade',
        }


class UsuarioEditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'email',)


class UsuarioEditPasswordForm(PasswordChangeForm):
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        user = self.user
        if not authenticate(username=user.username, password=old_password):
            raise forms.ValidationError("A senha atual está incorreta.")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("As senhas não coincidem.")

        return cleaned_data
