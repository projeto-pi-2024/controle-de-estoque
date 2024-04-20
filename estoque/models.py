from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    SITUACAO_CHOICES = (
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    )

    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_barras = models.CharField(max_length=100)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_inicial = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    situacao = models.CharField(
        max_length=10, choices=SITUACAO_CHOICES, default='Ativo')
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome


class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade_estoque = models.IntegerField()
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Estoque de {self.produto.nome}"
