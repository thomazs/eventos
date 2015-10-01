from django.contrib import admin

# Register your models here.
from .models import *

class CursosInline(admin.TabularInline):
    model = Curso

class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome','dt_inicio',
                    'dt_termino')
    search_fields = ('nome',)
    list_filter = ('situacao',)
    inlines = [CursosInline,]

admin.site.register(Evento, EventoAdmin)

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome_curso', 'carga_horaria', 'qtd_max_vagas')
    list_filter = ('evento',)
    search_fields = ('nome_curso',)

class InscricaoAdmin(admin.ModelAdmin):
    list_filter = ('evento',)
    search_fields = ('nome', 'cpf', 'rg')
    list_display = ('nome', 'telefone', 'email', 'evento')

admin.site.register(Curso, CursoAdmin)
admin.site.register(Inscricao, InscricaoAdmin)

