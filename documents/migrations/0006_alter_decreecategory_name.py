# Generated by Django 5.1.4 on 2025-02-19 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_alter_formplus_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decreecategory',
            name='name',
            field=models.CharField(max_length=999, unique=True, verbose_name='اسم الفئة'),
        ),
    ]
