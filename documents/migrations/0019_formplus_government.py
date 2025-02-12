# Generated by Django 5.1.4 on 2025-02-12 10:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0018_government'),
    ]

    operations = [
        migrations.AddField(
            model_name='formplus',
            name='government',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='documents.government'),
            preserve_default=False,
        ),
    ]
