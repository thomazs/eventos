# coding=utf-8

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from base.views import montaMensagemErro
from .models import Evento


from django.forms import ModelForm
class EventoForm(ModelForm):

    class Meta:
        model = Evento
        exclude = ('situacao',)

    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'campo'
            self.fields[f].widget.attrs['placeholder'] = self.fields[f].label
            self.fields[f].widget.attrs['title'] = self.fields[f].label
            self.fields[f].widget.attrs['data-toggle'] = 'tooltip'

def index(request):
    form = EventoForm()
    eventos_ativos = Evento.objects.filter(situacao__in=['2','5'])
    eventos_inativos = Evento.objects.filter(situacao='9')
    return render(request, 'index.html', locals())


def contato(request):
    return render(request, 'contato.html', locals())


def pesquisa_eventos(request):
    valor_pesquisado = request.GET.get('campo_busca','')
    resultados = Evento.objects.filter(nome__contains=valor_pesquisado)
    return render(request, 'pesquisa_eventos.html', locals())


def cria_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                'Seu evento foi adicionado! Aguarde entrarem em contato!')
        else:
            titulo = 'Cadastro de Evento'
            return render(request, 'forms.html', locals())
    return redirect(reverse_lazy('index'))

