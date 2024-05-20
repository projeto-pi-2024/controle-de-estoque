from django.shortcuts import render, get_object_or_404, redirect
from .models import Estoque, Categoria, Produto
from .forms import *
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse


@login_required
def home(request):
    # CARD - Totais ---------------------------------------------------------------------------------------------------
    produtos = Produto.objects.all()
    valor_total_custo_estoque = 0
    valor_total_venal_estoque = 0
    quantidade_total_estoque = 0

    # Iterar sobre todos os produtos
    for produto in produtos:
        # Calcular o estoque atual do produto considerando as movimentações de entrada e saída
        movimentacoes_entrada = Estoque.objects.filter(produto=produto, movimentacao='Entrada').aggregate(
            total_entrada=models.Sum('quantidade'))['total_entrada'] or 0
        movimentacoes_saida = Estoque.objects.filter(produto=produto, movimentacao='Saida').aggregate(
            total_saida=models.Sum('quantidade'))['total_saida'] or 0
        estoque_atual = movimentacoes_entrada - movimentacoes_saida

        # Adicionar o custo do produto multiplicado pelo estoque atual ao valor total do estoque em custo
        valor_total_custo_estoque += produto.custo * estoque_atual

        # Adicionar o valor de venda do produto multiplicado pelo estoque atual ao valor total do estoque venal
        valor_total_venal_estoque += produto.preco_venda * estoque_atual

        # Adicionar a quantidade em estoque atual à quantidade total de itens em estoque
        quantidade_total_estoque += estoque_atual

    # Contar a quantidade de categorias cadastradas
    quantidade_categorias = Categoria.objects.count()
    # -----------------------------------------------------------------------------------------------------------------

    # CARD - Últimas Movimentações ------------------------------------------------------------------------------------
    ultimas_movimentacoes = Estoque.objects.order_by('-criado_em')[:10]
    # -----------------------------------------------------------------------------------------------------------------

    # CARD - Quantidades Por Categorias -------------------------------------------------------------------------------
    categorias = Categoria.objects.all()

    # Criar um dicionário para armazenar o nome da categoria e a quantidade de produtos relacionados
    produtos_por_categorias = {}
    for categoria in categorias:
        quantidade_produtos = Produto.objects.filter(
            categoria=categoria).count()
        produtos_por_categorias[categoria] = quantidade_produtos
    # -----------------------------------------------------------------------------------------------------------------

    return render(request, 'home.html', {
        'valor_total_custo_estoque': valor_total_custo_estoque,
        'valor_total_venal_estoque': valor_total_venal_estoque,
        'quantidade_total_estoque': quantidade_total_estoque,
        'quantidade_categorias': quantidade_categorias,
        'ultimas_movimentacoes': ultimas_movimentacoes,
        'produtos_por_categorias': produtos_por_categorias,
    })


@login_required
def estoque(request):
    # 'q' é o campo de pesquisa no formulário
    pesquisa = request.GET.get('q', '')

    produtos = Produto.objects.order_by('id')

    if pesquisa:
        # Filtra os produtos pelo nome usando 'icontains' para pesquisa parcial
        produtos = produtos.filter(nome__icontains=pesquisa)

    paginacao = Paginator(produtos, 10)
    pagina = request.GET.get('page')
    page_obj = paginacao.get_page(pagina)

    context = {
        'page_obj': page_obj,
        'pesquisa': pesquisa,
    }

    return render(request, 'estoque.html', context)


@login_required
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


@login_required
def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso.')
            return redirect('categorias')
        messages.error(request, 'Erro ao criar categoria. Por favor, tente novamente.')
    else:
        form = CategoriaForm()

    return render(request, 'criar_categoria.html', {'form': form})


@login_required
def atualizar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso.')
        else:
            messages.error(request, 'Erro ao atualizar a categoria. Por favor, tente novamente.')
        return redirect('categorias')
    else:
        form = CategoriaForm(instance=categoria)

    context = {'form': form, 'categoria': categoria}
    return render(request, 'atualizar_categoria.html', context)


@login_required(login_url='login')
def excluir_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    # Verifica se existem produtos relacionados à categoria
    if Produto.objects.filter(categoria=categoria).exists():
        messages.error(request, 'Não é possível excluir esta categoria porque existem produtos relacionados a ela.')
        return redirect(reverse('atualizar_categoria', args=[str(categoria.id)]))
    else:
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso.')
        return redirect('categorias')


@login_required
def produto(request):
    return render(request, 'produto.html')


@login_required
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
            messages.success(request, 'Produto criado com sucesso.')

            return redirect('estoque')
        messages.error(request, 'Erro ao criar o produto. Por favor, tente novamente.')
    else:
        form = ProdutoForm()

    context = {'form': form, 'categorias': categorias}

    return render(request, 'criar_produto.html', context)


@login_required
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
            messages.success(request, 'Produto atualizado com sucesso.')
            return redirect('estoque')
        messages.error(request, 'Erro ao atualizar o produto. Por favor, tente novamente.')
    else:
        form = ProdutoForm(instance=produto)

    context = {'form': form, 'categorias': categorias}

    return render(request, 'atualizar_produto.html', context)


@login_required
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
            messages.success(request, 'Estoque atualizado com sucesso.')

            return redirect('estoque')
        messages.error(request, 'Erro ao atualizar o estoque. Por favor, tente novamente.')
    else:
        form = EstoqueForm()

    context = {'form': form, 'produto': produto}

    return render(request, 'entrada_saida_estoque.html', context)


def login_view(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('/')

    context = {
        'form': form
    }

    return render(
        request,
        'login.html',
        context,
    )


@login_required(login_url='login')
def logout_view(request):
    auth.logout(request)

    return redirect('login')


@login_required(login_url='login')
def user_change_profile(request):
    if request.method == 'POST':
        form = UsuarioEditProfileForm(data=request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Perfil atualizado com sucesso.')
            return redirect('/')
        else:
            messages.error(request, 'Erro ao atualizar o perfil. Por favor, tente novamente.')
            return render(request, 'user_update_profile.html')

    else:
        form = UsuarioEditProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, 'user_update_profile.html', context)


@login_required(login_url='login')
def user_change_password(request):
    if request.method == 'POST':
        form = UsuarioEditPasswordForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Senha atualizada com sucesso.')
            return redirect('/')
        else:
            messages.error(request, 'Erro ao atualizar a senha. Por favor, tente novamente.')
            return render(request, 'user_update_password.html', {'form': form})

    else:
        form = UsuarioEditPasswordForm(user=request.user)
        context = {'form': form}
        return render(request, 'user_update_password.html', context)
    
def sobre(request):
    return render(request, 'sobre.html') 