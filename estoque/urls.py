from django.urls import path
from . import views
# from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete


urlpatterns = [
    path('', views.home, name='home'),
    path('estoque/', views.estoque, name='estoque'),
    path('categorias/', views.categorias, name='categorias'),

    # PRODUTO CRUD
    path('produtos/criar-produto', views.criar_produto, name='criar_produto'),
    path('produtos/atualizar-produto/<int:produto_id>/',
         views.atualizar_produto, name='atualizar_produto'),

    # ESTOQUE
    path('estoque/atualizar-estoque/<int:produto_id>/', views.entrada_saida_estoque, name='entrada_saida_estoque'),

    # CATEGORIA CRUD
    path('categorias/criar-categoria/', views.criar_categoria, name='criar_categoria'),
    path('categorias/atualizar-categoria/<int:categoria_id>/', views.atualizar_categoria, name='atualizar_categoria'),

    # USUARIO
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/user-update/', views.user_change_profile, name='user_change_profile'),
    path('accounts/user-update/password-change', views.user_change_password, name='user_change_password'),
    # path('accounts/user-update/password-reset/', password_reset, name='password_reset'),
    # path('accounts/user-update/password-reset/done/', password_reset_done, name='password_reset_done'),
    # path('accounts/user-update/password-reset/confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    # path('accounts/reset/done/', password_reset_complete, name='password_reset_complete'),
    # path('user/create/', views.register, name='register'),
    # path('user/update/', views.user_update, name='user_update'),
]
