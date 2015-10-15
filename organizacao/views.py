# coding=utf-8
from datetime import datetime

from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView
from base.views import montaMensagemErro
from .models import Evento, Inscricao

from django.forms import ModelForm, ValidationError


class ModelFormBase(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelFormBase, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'campo'
            self.fields[f].widget.attrs['placeholder'] = self.fields[f].label
            self.fields[f].widget.attrs['title'] = self.fields[f].label


class EventoForm(ModelFormBase):

    class Meta:
        model = Evento
        exclude = ('situacao',)

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

from django.forms import HiddenInput
class InscricaoForm(ModelFormBase):
    class Meta:
        model = Inscricao
        exclude = ('status',)
    def __init__(self, *args, **kwargs):
        super(InscricaoForm, self).__init__(*args, **kwargs)
        self.fields['evento'].widget = HiddenInput()
        ev = self.initial['evento'];
        self.fields['cursos'].queryset = self.fields['cursos'].queryset.filter(evento_id=ev.id)


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

from django.http import Http404
from django.shortcuts import get_object_or_404

def detalhe_evento(request, id):
    evento = get_object_or_404(Evento, pk=id)
    return render(request, 'detalheevento.html', locals())


def inscreve_evento(request, id):
    voltar = reverse_lazy('detalhe_evento', args=[id])
    evento = get_object_or_404(Evento, pk=id)
    titulo = u'Inscrições - %s' % evento
    form = InscricaoForm(initial={'evento':evento})
    if request.method == 'POST':
        form = InscricaoForm(request.POST);
        if form.is_valid():
            s = form.save()
            s.evento = evento
            s.save()
            messages.success(request,
                u'Inscrição realizada com sucesso!')
            return redirect(reverse_lazy('index'))
    return render(request, 'forms.html', locals())
