# Generated by Django 5.1.4 on 2025-02-12 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0017_formplus_objection_phone_objection_reason_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Government',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
