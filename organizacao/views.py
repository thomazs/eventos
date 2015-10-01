# coding=utf-8
from datetime import datetime

from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from base.views import montaMensagemErro
from .models import Evento


from django.forms import ModelForm, ValidationError
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

    def clean(self):
        data = super(EventoForm, self).clean()
        if data.get('dt_termino',None) and data.get('dt_inicio') and \
                        data['dt_termino'] < data['dt_inicio']:
            raise ValidationError('Data de Término deve ser maior ou igual a Data de Início')

        if data.get('dt_inicio') and data['dt_inicio'].date() < datetime.now().date():
             raise ValidationError('Data de Início deve ser maior ou igual a data atual')
        # if data.get('dt_inicio') and data['dt_inicio'] < datetime.now():
        #     raise ValidationError('Data de Início deve ser maior ou igual a data atual')

        return data


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

def detalhe_evento(request, id):
    evento = Evento.objects.get(pk=id)
    return render(request, 'detalheevento.html', locals())