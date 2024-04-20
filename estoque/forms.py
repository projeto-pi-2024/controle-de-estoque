from django import forms
from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'custo', 'codigo_barras',
                  'preco_venda', 'quantidade_inicial', 'categoria']
