from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from PFI import views

urlpatterns = [
    # -------------------------
    # Admin Django
    # -------------------------
    path('admin/', admin.site.urls),

    # -------------------------
    # Home
    # -------------------------
    path('', views.home, name='home'),

    # -------------------------
    # Autenticação manual
    # -------------------------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='deslogar'),
    path('registrar/', views.registrar, name='registrar'),

    # -------------------------
    # Páginas de usuário
    # -------------------------
    path('adm/', views.pagina_adm, name='adm_dashboard'),
    path('cliente/', views.cliente, name='cliente'),  # <-- apontando para view cliente correta
    path('editar_meus_dados_adm/', views.editar_meus_dados_adm, name='editar_meus_dados_adm'),
    path('editar_meus_dados_usuario/', views.editar_meus_dados_usuario, name='editar_meus_dados_usuario'),

    # -------------------------
    # Carrossel
    # -------------------------
    path('carrosel/', views.editar_carrossel, name='editar_carrossel'),
    path('carrosel/adicionar/', views.adicionar_imagem, name='adicionar_imagem'),
    path('carrosel/editar/<int:imagem_id>/', views.editar_imagem, name='editar_imagem'),
    path('carrosel/ativar/<int:id>/', views.ativar_imagem, name='ativar_imagem'),
    path('carrosel/remover/<int:imagem_id>/', views.remover_imagem, name='remover_imagem'),

    # -------------------------
    # Usuários
    # -------------------------
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/adicionar/', views.adicionar_usuario, name='adicionar_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/excluir/<int:id>/', views.excluir_usuario, name='excluir_usuario'),

    # -------------------------
    # Produtos
    # -------------------------
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('produtos/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path("produtos/editar/<int:id>/", views.editar_produto, name="editar_produto"),
    path('produtos/excluir/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
    path('produtos/adicionar_estoque/<int:produto_id>/', views.adicionar_estoque, name='adicionar_estoque'),

    # -------------------------
    # Dívidas e histórico
    # -------------------------
    path("minhas-dividas/", views.minhas_dividas_usuario, name="minhas_dividas_usuario"),
    path('dividas/', views.minhas_dividas, name='minhas_dividas'),
    path('dividas/<str:matricula>/registrar_pagamento/', views.registrar_pagamento, name='registrar_pagamento'),
    path('historico/', views.historico_usuario, name='historico'),
    path('historico_adm/', views.historico_adm, name='historico_adm'),

    # -------------------------
    # Vendas
    # -------------------------
    path('vendas/', views.vendas_view, name='vendas'),

    # -------------------------
    # API
    # -------------------------
    path("api/usuario/", views.api_buscar_usuario, name="api_buscar_usuario"),
    path("api/registrar_venda/", views.api_registrar_venda, name="api_registrar_venda"),
    path("api/produtos/", views.api_listar_produtos, name="api_listar_produtos"),

    path('relatorio/', views.gerar_relatorio, name='gerar_relatorio'),
    path('exportar_relatorio/', views.exportar_relatorio, name='exportar_relatorio'),

]

# Servir arquivos de mídia em DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)