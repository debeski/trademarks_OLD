# Generated by Django 5.1.4 on 2025-02-27 15:16

import django.core.validators
import documents.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0010_alter_decree_applicant_alter_decree_ar_brand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decree',
            name='attach',
            field=models.FileField(blank=True, upload_to=documents.models.generate_random_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'], message='يرجى رفع ملف PDF فقط.')], verbose_name='المرفقات'),
        ),
        migrations.AlterField(
            model_name='decree',
            name='number_canceled',
            field=models.CharField(blank=True, null=True, verbose_name='رقم القرار المسحوب او الملغي'),
        ),
        migrations.AlterField(
            model_name='decree',
            name='pdf_file',
            field=models.FileField(blank=True, upload_to=documents.models.generate_random_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'], message='يرجى رفع ملف PDF فقط.')], verbose_name='ملف القرار'),
        ),
        migrations.AlterField(
            model_name='formplus',
            name='pdf_file',
            field=models.FileField(upload_to=documents.models.generate_random_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'], message='يرجى رفع ملف PDF فقط.')], verbose_name='ملف PDF'),
        ),
        migrations.AlterField(
            model_name='formplus',
            name='word_file',
            field=models.FileField(blank=True, upload_to=documents.models.generate_random_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['doc', 'docx'], message='يرجى رفع ملف Word فقط.')], verbose_name='ملف Word'),
        ),
        migrations.AlterField(
            model_name='objection',
            name='pdf_file',
            field=models.FileField(blank=True, upload_to=documents.models.generate_random_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'], message='يرجى رفع ملف PDF فقط.')], verbose_name='ملف الاعتراض'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='attach',
            field=models.FileField(blank=True, upload_to=documents.models.generate_random_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'], message='يرجى رفع ملف PDF فقط.')], verbose_name='المرفقات'),
        ),
    ]
