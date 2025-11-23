# cantina/forms.py
from django import forms
from .models import Usuario
from django.contrib.auth.forms import AuthenticationForm

from .models import Usuario

# cantina/forms.py
from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(),
        required=False,
        help_text="Deixe em branco se não quiser alterar a senha."
    )
    senhaConfirm = forms.CharField(
        label="Confirme a senha",
        widget=forms.PasswordInput(),
        required=False
    )
    foto = forms.ImageField(
        label="Foto",
        required=False
    )

    class Meta:
        model = Usuario
        fields = [
            "nome", "matricula", "telefone", "telefone_responsavel",
            "email", "senha", "is_admin", "foto"
        ]
        labels = {
            "telefone_responsavel": "Telefone do Responsável",
            "is_admin": "É administrador?",
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senhaConfirm = cleaned_data.get("senhaConfirm")

        if senha or senhaConfirm:
            if senha != senhaConfirm:
                raise forms.ValidationError("As senhas não conferem!")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Matrícula ou E-mail",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite sua matrícula ou E-mail'
        })
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Digite sua senha'
        })
    )
from .models import ImagemCarrossel

class ImagemCarrosselForm(forms.ModelForm):
    class Meta:
        model = ImagemCarrossel
        fields = ['titulo', 'imagem', 'ativo']

from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco_compra', 'preco_venda', 'foto', 'estoque']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input'}),
            'descricao': forms.Textarea(attrs={'class': 'input'}),
            'preco_compra': forms.NumberInput(attrs={'step': '0.01', 'class': 'input'}),
            'preco_venda': forms.NumberInput(attrs={'step': '0.01', 'class': 'input'}),
            'estoque': forms.NumberInput(attrs={'class': 'input'}),
        }
