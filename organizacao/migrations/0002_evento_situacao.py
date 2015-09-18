# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizacao', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='situacao',
            field=models.CharField(default=b'1', max_length=1, verbose_name='Situa\xe7\xe3o', choices=[(b'1', b'Aguardando'), (b'2', b'Confirmado'), (b'5', b'Ativo'), (b'9', b'Inativo')]),
        ),
    ]
