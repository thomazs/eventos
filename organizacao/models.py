# coding=utf-8
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.conf import settings


class Evento(models.Model):

    class Meta:
        db_table = 'evento'

    SITUACAO_CHOICES = (('1','Aguardando'),('2','Confirmado'),
                        ('3','Esgotado'),
                        ('5','Ativo'),('9','Inativo'),)

    nome = models.CharField('Nome do Evento', max_length=250,)
    dt_inicio = models.DateTimeField(u'Dt.Início')
    dt_termino = models.DateTimeField(u'Dt.Término')
    informacoes = models.TextField(u'Informações')
    situacao = models.CharField(u'Situação', max_length=1,
                                choices=SITUACAO_CHOICES, default='1')
    nome_contato = models.CharField('Nome do Contato', max_length=80)
    email = models.EmailField('Email do Contato', max_length=250)
    telefone = models.CharField('Telefone', max_length=20)
    qtd_participantes = models.IntegerField('Qtd.Participantes',
                                            null=True, blank=True,
                                            editable=False)

    def __unicode__(self):
        return self.nome

    def __str__(self):
        return self.nome

    @property
    def data(self):
        return self.dt_inicio.strftime("%d/%m/%Y")

    @property
    def hora(self):
        return self.dt_inicio.strftime("%H:%M:%S")

    @property
    def esgotado(self):
        return self.situacao == '3'


class Curso(models.Model):

    class Meta:
        db_table = 'curso'

    evento = models.ForeignKey(Evento,related_name='curso_set')
    nome_curso = models.CharField('Nome do Curso', max_length=250)
    carga_horaria = models.IntegerField(u'Carga Horária')
    instrutor = models.CharField('Instrutor', max_length=100,
                                 null=True, blank=True)
    data = models.DateField('Data do Curso', null=True, blank=True)
    hora = models.TimeField('Hora', null=True, blank=True)
    qtd_max_vagas = models.IntegerField(u'Qtd.Máx.Vagas')

    def __unicode__(self):
        return self.nome_curso

    def __str__(self):
        return self.nome_curso

    @property
    def vagas_disponiveis(self):
        return self.qtd_max_vagas - \
               self.inscritoscurso_set.all().count()


class Inscricao(models.Model):

    class Meta:
        db_table = 'inscricao'
        verbose_name = u'inscrição'
        verbose_name_plural = u'inscrições'
    evento = models.ForeignKey(Evento,
                               related_name='inscricao_set')
    nome = models.CharField('Nome', max_length=100)
    cpf = models.CharField('CPF', max_length=14, unique=True, null=True, blank=True)
    rg = models.CharField('RG', max_length=20, null=True, blank=True)
    pai = models.CharField('Nome do Pai', max_length=100, null=True, blank=True)
    mae = models.CharField(u'Nome da Mãe', max_length=100, null=True, blank=True)
    email = models.EmailField('Email', max_length=250)
    telefone = models.CharField('Telefone', max_length=20)
    status = models.BooleanField('Aceita', default=False)
    cursos = models.ManyToManyField(Curso, related_name='inscritoscurso_set')
    data_cadastro = models.DateTimeField("Dt.Cadastro", auto_now_add=True, null=True, blank=True)
    data_modificacao = models.DateTimeField("Dt.Últ.Modificação", auto_now=True, null=True, blank=True)
    ip = models.IPAddressField("IP", editable=False, null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, editable=False)

    def __unicode__(self):
        return (self.evento.nome)+'-'+self.nome

    def __str__(self):
        return  self.nome




## SIGNALS

def ajusta_status(sender, instance, *args, **kwargs):
    ev = Evento.objects.get(pk=instance.evento.pk)
    if ev.situacao != '3' and \
        ev.qtd_participantes <= ev.inscricao_set.all().count():
        ev.situacao = '3'
        ev.save()
    elif ev.situacao == '3' and \
        ev.qtd_participantes > ev.inscricao_set.all().count():
        ev.situacao = '5'
        ev.save()


post_save.connect(ajusta_status, Inscricao)
post_delete.connect(ajusta_status, Inscricao)

def enviar_notificacao_evento(evento_id):
    pass