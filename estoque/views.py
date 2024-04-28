from django.shortcuts import render, get_object_or_404, redirect
from .models import Estoque, Categoria, Produto
from .forms import *
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator


def home(request):
    return render(request, 'home.html')


def estoque(request):    
    pesquisa = request.POST.get('pesquisa', '')
    produtos = Produto.objects.order_by('id')

    if pesquisa:
        # Filtra os produtos pelo nome usando 'icontains' para pesquisa parcial
        produtos = produtos.filter(nome__icontains=pesquisa)

    paginacao = Paginator(produtos, 10)
    pagina = request.GET.get('page')
    page_obj = paginacao.get_page(pagina)

    context = {'page_obj': page_obj, }

    if pesquisa:
        # Adiciona a variável pesquisa em context apenas se esta estiver definida
        context['pesquisa'] = pesquisa 

    return render(request, 'estoque.html', context)


def categorias(request):
    categorias = Categoria.objects.annotate(
        quantidade_produtos=Count('produto'),
        quantidade_estoque=Coalesce(Sum('produto__quantidade_estoque'), 0)
    ).order_by('id')
    
    paginacao = Paginator(categorias, 10)
    pagina = request.GET.get('page')
    page_obj = paginacao.get_page(pagina)

    context = {'page_obj': page_obj}

    return render(request, 'categorias.html', context)


def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    else:
        form = CategoriaForm()

    return render(request, 'criar_categoria.html', {'form': form})


def atualizar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
        return redirect('categorias')
    else:
        form = CategoriaForm(instance=categoria)

    context = {'form': form, 'categoria': categoria}
    return render(request, 'atualizar_categoria.html', context)


def produto(request):
    return render(request, 'produto.html')


def criar_produto(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['preco_venda'] = request.POST['preco_venda'].replace('.', '').replace(
            ',', '.')
        request.POST['custo'] = request.POST['custo'].replace(
            '.', '').replace(',', '.')

        form = ProdutoForm(request.POST)

        if form.is_valid():
            produto = form.save(commit=False)
            produto.save()

            Estoque.objects.create(
                produto=produto,
                movimentacao='Entrada',
                quantidade=produto.quantidade_inicial
            )

            produto.quantidade_estoque = produto.quantidade_inicial
            produto.save()

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


def entrada_saida_estoque(request, produto_id):
    produto = Produto.objects.get(pk=produto_id)

    if request.method == 'POST':
        form = EstoqueForm(request.POST)
        if form.is_valid():
            movimentacao = form.cleaned_data['movimentacao']
            quantidade = form.cleaned_data['quantidade']

            if movimentacao == 'Entrada':
                produto.quantidade_estoque += quantidade
            elif movimentacao == 'Saida':
                if quantidade > produto.quantidade_estoque:
                    form.add_error(
                        'quantidade', 'A quantidade de saída não pode ser maior que o estoque total')

                    context = {'form': form, 'produto': produto}
                    return render(request, 'entrada_saida_estoque.html', context)

                produto.quantidade_estoque -= quantidade

            produto.save()

            Estoque.objects.create(
                produto=produto,
                movimentacao=movimentacao,
                quantidade=quantidade
            )

            return redirect('estoque')
    else:
        form = EstoqueForm()

    context = {'form': form, 'produto': produto}

    return render(request, 'entrada_saida_estoque.html', context)
