"""
URL configuration for registreon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from ocorrencias import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #Página Inicial
    path('', views.inicio, name='inicio'),

    #Ocorrência
    path('ocorrencias/', views.ocorrencias, name='ocorrencias'),

    #Cadstro e Login cidadão
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_cidadao, name='logout_cidadao'),

    path('anonimo/', views.anonimo, name='anonimo'),

    path('painel-cidadao/', views.painel_cidadao, name='painel_cidadao'),  
    path(
        'painel-cidadao/solicitacao/<int:num_solicitacao>/',
        views.detalhe_cidadao,
        name='detalhe_cidadao'
    ),

    #Login do funcionário
    path('funcionario/', views.funcionario_login, name='funcionario_login'),

    path(
        'painel-funcionario/',
        views.PainelFuncionarioView.as_view(),
        name='painel_funcionario'
    ),
    path(
        'funcionario/sair/',
        views.logout_funcionario,
        name='logout_funcionario'
    ),

path('ocorrencia/<int:pk>/', views.DetalheOcorrenciaView.as_view(), name='detalhe_ocorrencia'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
