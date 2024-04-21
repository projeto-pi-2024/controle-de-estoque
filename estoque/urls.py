from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('estoque/', views.estoque, name='estoque'),
    # path('produto/', views.produto, name='produto'),  # talvez nao ter
    path('categorias/', views.categorias, name='categorias'),

    # PRODUTO CRUD
    path('produtos/criar-produto', views.criar_produto, name='criar_produto'),
    path('produtos/atualizar-produto/<int:produto_id>/', views.atualizar_produto, name='atualizar_produto'),
    
    # ESTOQUE
    path('estoque/atualizar-estoque/<int:produto_id>/', views.entrada_saida_estoque, name='entrada_saida_estoque'),

    # CATEGORIA CRUD
    path('categorias/criar-categoria/', views.criar_categoria, name='criar_categoria'),
    path('categorias/atualizar-categoria/<int:categoria_id>/', views.atualizar_categoria, name='atualizar_categoria'),
]
