# coding=utf-8
from django.db import models

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
    cursos = models.ManyToManyField(Curso)

    def __unicode__(self):
        return (self.evento.nome)+'-'+self.nome

    def __str__(self):
        return  self.nome



