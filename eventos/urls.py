"""eventos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'organizacao.views.index', name='index'),
    url(r'^contato/$', 'organizacao.views.contato', name='contato'),
    url(r'^pesquisa_eventos/$',
        'organizacao.views.pesquisa_eventos',
        name='pesquisa_eventos'),
    url(r'^criaevento/$', 'organizacao.views.cria_evento', name='criaevento'),
    url(r'^evento/(?P<id>\d+)/$',
        'organizacao.views.detalhe_evento',
        name='detalhe_evento'),
    url(r'^evento/(?P<id>\d+)/inscricao/$', 'organizacao.views.inscreve_evento',
        name='inscreve_evento'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
