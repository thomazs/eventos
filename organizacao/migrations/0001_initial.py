# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=250, verbose_name=b'Nome')),
                ('dt_inicio', models.DateTimeField(verbose_name='Dt.In\xedcio')),
                ('dt_termino', models.DateTimeField(verbose_name='Dt.T\xe9rmino')),
                ('informacoes', models.TextField(verbose_name='Informa\xe7\xf5es')),
            ],
            options={
                'db_table': 'evento',
            },
        ),
    ]
