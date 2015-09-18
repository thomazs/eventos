from django.contrib import admin

# Register your models here.
from .models import *

class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome','dt_inicio',
                    'dt_termino')
    search_fields = ('nome',)

admin.site.register(Evento, EventoAdmin)

# class CursoAdmin(admin.ModelAdmin):
#     pass
#
# class InscricaoAdmin(admin.ModelAdmin):
#     pass
#
# admin.site.register(Curso, CursoAdmin)
# admin.site.register(Inscricao, InscricaoAdmin)
#
