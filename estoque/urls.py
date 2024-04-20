from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('estoque/', views.estoque, name='estoque'),
    path('produto/', views.produto, name='produto'), # talvez nao ter
    path('categorias/', views.categorias, name='categorias'),

    # contact CRUD
    # path('produto/criar-produto/', views.criar_produto, name='criar_produto'),
    # path('produto/<int:produto_id>/atualizar-produto/', views.atualizar_produto, name='atualizar_produto'),

    # path('produto/criar-categoria/', views.criar_categoria, name='criar_categoria'),
    # path('produto/<int:produto_id>/atualizar-categoria/', views.atualizar_categoria, name='atualizar_categoria'),

]
