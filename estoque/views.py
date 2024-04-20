from django.shortcuts import render, get_object_or_404, redirect
from .models import Estoque, Categoria, Produto
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .forms import ProdutoForm
from django.urls import reverse


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


def criar_produto(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save()
            Estoque.objects.create(
                produto=produto, quantidade_estoque=produto.quantidade_inicial)
            return redirect('estoque')
    else:
        form = ProdutoForm()

    context = {'form': form, 'categorias': categorias}
    return render(request, 'criar_produto.html', context)


def atualizar_produto(request, produto_id):
    categorias = Categoria.objects.all()

    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['preco_venda'] = request.POST['preco_venda'].replace(
            ',', '.')
        request.POST['custo'] = request.POST['custo'].replace(',', '.')
        
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('estoque')
    else:
        form = ProdutoForm(instance=produto)

    context = {'form': form, 'categorias': categorias}
    return render(request, 'atualizar_produto.html', context)
