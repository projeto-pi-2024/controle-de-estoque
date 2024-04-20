from django.shortcuts import render, get_object_or_404, redirect
from .models import Estoque, Categoria, Produto
from django.db.models import Count


def home(request):
    return render(request, 'home.html')


def estoque(request):
    produtos = Produto.objects.order_by('-nome')

    for produto in produtos:
        estoque_produto = Estoque.objects.filter(produto=produto).first()
        produto.quantidade_em_estoque = estoque_produto.quantidade_estoque if estoque_produto else 0

    context = {'produtos': produtos, }

    return render(request, 'estoque.html', context)


def categorias(request):
    categorias = Categoria.objects.annotate(num_produtos=Count('produto'))

    context = {'categorias': categorias}

    return render(request, 'categorias.html', context)


def produto(request):
    return render(request, 'produto.html')
