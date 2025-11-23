from django.contrib import admin
from .models import Produto, Venda, ItemVenda, Usuario, ImagemCarrossel, EntradaEstoque

admin.site.register(Produto)
admin.site.register(Venda)
admin.site.register(ItemVenda)
admin.site.register(Usuario)
admin.site.register(ImagemCarrossel)
admin.site.register(EntradaEstoque)