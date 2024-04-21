from django.contrib import admin
from .models import Categoria, Estoque, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'criado_em')
    list_filter = ('criado_em',)
    ordering = ('-id',)
    search_fields = ('id', 'nome',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_barras', 'nome', 'descricao', 'custo', 'preco_venda',
                    'quantidade_inicial', 'quantidade_estoque', 'categoria', 'situacao', 'criado_em',)
    list_filter = ('criado_em',)
    ordering = ('-id',)
    search_fields = ('id', 'nome',)
    list_per_page = 30
    list_max_show_all = 100


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'movimentacao', 'quantidade', 'criado_em')
    list_filter = ('criado_em',)
    ordering = ('-id',)
    search_fields = ('id', 'produto',)
    list_per_page = 30
    list_max_show_all = 100
