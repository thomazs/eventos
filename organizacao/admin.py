# coding=utf-8

from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from .models import *

class CursosInline(admin.TabularInline):
    model = Curso

class EventoAdmin(admin.ModelAdmin):
    def preenchidas(self, obj):
        return Inscricao.objects.filter(evento=obj).count()
    list_display = ('nome','dt_inicio',
                    'dt_termino', 'qtd_participantes',
                    'preenchidas',)

    search_fields = ('nome',
    )
    list_filter = ('situacao',)


    inlines = [CursosInline,]
    actions = ['action_autorizar', 'action_inativar']
    actions_on_bottom = True

    action_autorizar = lambda self, modeladmin, request, queryset: \
        queryset.update(status=5)
    action_autorizar.short_description = 'Autorizar Eventos'

    action_inativar = lambda self, modeladmin, request, queryset: \
        queryset.update(status=9)
    action_inativar.short_description = 'Inativar Eventos'

admin.site.register(Evento, EventoAdmin)

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome_curso', 'carga_horaria', 'qtd_max_vagas')
    list_filter = ('evento',)
    search_fields = ('nome_curso',)


"""
    Inscricao.objects.filter(evento__in=
        Evento.objects.filter(
            situacao__in=['2','3','5'],
            nome__icontains='py'
        )
    )
    Inscricao.objects.filter(
        evento__situacao__in=['2','3','5'],
        evento__nome__icontains='py'
    )
"""

class InscricoesEventoPythonFilter(admin.SimpleListFilter):
    title = 'Eventos Python'  # indica o nome do filtro
    parameter_name = 'evpy'  # indica qual o nome do parâmetro que aparece na URL

    def lookups(self, request, model_admin):
        """
        Indica quais valores aparecem como opções para os filtros
        """
        return (
            ('A', 'Eventos Python - Todos'),
            ('E', 'Eventos Python - Esgotados'),
            ('I', 'Eventos Python - Inativos/Cancelados'),
        )

    def queryset(self, request, queryset):
        """
        Indica qual filtro deve ser realizado
        """
        i = []
        if self.value() == 'A':
            i = ['2','3','5','9']
        elif self.value() == 'E':
            i = ['3']
        if self.value() == 'I':
            i = ['9']
        if i:
            return queryset.filter(
                evento__situacao__in=i,
                evento__nome__icontains='py'
            )
        return queryset
    #
    # def queryset(self, request, queryset):
    #     """
    #     Indica qual filtro deve ser realizado
    #     """
    #     if self.value() == 'A':
    #             return queryset.filter(
    #                 evento__situacao__in=['2','3','5','9'],
    #                 evento__nome__icontains='py'
    #             )
    #
    #     if self.value() == 'E':
    #             return queryset.filter(
    #                 evento__situacao='3',
    #                 evento__nome__icontains='py'
    #             )
    #
    #     if self.value() == 'I':
    #             return queryset.filter(
    #                 evento__situacao='9',
    #                 evento__nome__icontains='py'
    #             )
    #
    #     return queryset



class InscricaoAdmin(admin.ModelAdmin):
    list_filter = ('evento','evento__situacao',InscricoesEventoPythonFilter)
    search_fields = ('nome', 'cpf', 'rg')
    list_display = ('nome', 'telefone', 'email', 'link_evento')
    def link_evento(self, obj):
        url = reverse_lazy("admin:organizacao_evento_changelist")
        return """<a href='%s'>%s</a>""" %(url, obj.evento)
    link_evento.short_description = 'Evento'
    link_evento.allow_tags = True

    def save_model(self, request, obj, form, change):
        obj.ip = request.META['REMOTE_ADDR']
        obj.usuario = request.user if request.user.is_authenticated() \
                else None
        super(InscricaoAdmin, self).save_model(request, obj, form, change)

admin.site.register(Curso, CursoAdmin)
admin.site.register(Inscricao, InscricaoAdmin)

