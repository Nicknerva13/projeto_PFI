# --------------------------
# Usuário
# --------------------------
from typing import Any

from django.db import models
from django.utils import timezone
from datetime import timedelta

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    telefone_responsavel = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)

    saldo_em_dividas = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    data_primeira_compra = models.DateField(null=True, blank=True)

    # NOVO CAMPO PARA FOTO
    foto = models.ImageField(upload_to='fotos_usuarios/', blank=True, null=True)

    def limite_disponivel(self):
        return max(0, 30 - float(self.saldo_em_dividas))

    def vencimento(self):
        """Data de vencimento baseada na primeira compra fiada."""
        if self.data_primeira_compra:
            return self.data_primeira_compra + timedelta(days=30)
        return timezone.now().date() + timedelta(days=30)

    def __str__(self):
        return f"{self.nome} ({'Admin' if self.is_admin else 'Usuário'})"



# --------------------------
# Produto
# --------------------------
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    preco_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    foto = models.ImageField(upload_to="produtos/", blank=True, null=True)

    estoque = models.IntegerField(default=0)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)
        self.preco = None

    def __str__(self):
        return self.nome



# --------------------------
# Venda e Itens da Venda
# --------------------------
class Venda(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comprador')
    vendedor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendedor')
    valor_total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    pago = models.BooleanField(default=False)
    metodo_pagamento = models.CharField(
        max_length=20,
        choices=[('fiado','Fiado'), ('pix','Pix'), ('dinheiro','Dinheiro')],
        default='fiado'
    )
    data = models.DateTimeField(auto_now_add=True)


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}x"

# --------------------------
# Imagens do Carrossel
# --------------------------
class ImagemCarrossel(models.Model):
    titulo = models.CharField(max_length=100, blank=True, null=True)
    imagem = models.ImageField(upload_to='carrossel/')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo or f"Imagem {self.id}"


# --------------------------
# Dívidas
# --------------------------
class Divida(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name="dividas")
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    pago = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    juros_ativo = models.BooleanField(default=False)

    def vencimento(self):
        return self.data_criacao + timedelta(days=30)

    def dias_restantes(self):
        return (self.vencimento() - timezone.now()).days

    def aplicar_juros(self):
        """Aplica juros de 10% se vencida e ainda não aplicado."""
        if not self.pago and not self.juros_ativo and self.dias_restantes() < 0:
            self.valor *= 1.10
            self.juros_ativo = True
            self.save()

    def __str__(self):
        return f"{self.usuario.nome} - {self.descricao} - R${self.valor:.2f}"


# --------------------------
# Histórico de Compras
# --------------------------
class HistoricoCompra(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name="historico_compras")
    produto = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nome} - {self.produto} - R${self.valor:.2f}"

class Pagamento(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=50)
    data_pagamento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nome} - R$ {self.valor_pago}"


class EntradaEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)

    def valor_total(self):
        return self.quantidade * self.preco_unitario
