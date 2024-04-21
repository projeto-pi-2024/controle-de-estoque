from django import forms
from .models import *


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'custo', 'codigo_barras',
                  'preco_venda', 'quantidade_inicial', 'categoria']


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
