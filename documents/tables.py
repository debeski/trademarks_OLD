import os
from django.utils.html import mark_safe
import django_tables2 as tables
from .models import Decree, Publication, Objection, FormPlus, Country, Government, ComType, DocType
from django.urls import reverse
# from django.utils.safestring import mark_safe
# from babel.dates import format_date


class GovernmentTable(tables.Table):
    edit = tables.Column(accessor='id', verbose_name='', empty_values=())

    def __init__(self, *args, model_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name

    class Meta:
        model = Government
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'edit')
        attrs = {'class': 'table table-hover table-responsive align-middle table-sm'}

    def render_edit(self, value):
        base_url = reverse("manage_sections")
        # Derive model name from the Meta.model class name
        model_name = self.Meta.model.__name__
        url = f"{base_url}?model={model_name}&id={value}"
        return mark_safe(f'<a href="{url}" class="btn btn-secondary">تعديل</a>')

class CountryTable(tables.Table):
    edit = tables.Column(accessor='id', verbose_name='', empty_values=())

    def __init__(self, *args, model_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name

    class Meta:
        model = Country
        template_name = "django_tables2/bootstrap5.html"
        fields = ('en_name', 'ar_name', 'edit')
        attrs = {'class': 'table table-hover table-responsive align-middle table-sm'}

    def render_edit(self, value):
        base_url = reverse("manage_sections")
        # Derive model name from the Meta.model class name
        model_name = self.Meta.model.__name__
        url = f"{base_url}?model={model_name}&id={value}"
        return mark_safe(f'<a href="{url}" class="btn btn-secondary">تعديل</a>')

class ComTypeTable(tables.Table):
    edit = tables.Column(accessor='id', verbose_name='', empty_values=())

    def __init__(self, *args, model_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name

    class Meta:
        model = ComType
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'edit')
        attrs = {'class': 'table table-hover table-responsive align-middle table-sm'}

    def render_edit(self, value):
        base_url = reverse("manage_sections")
        # Derive model name from the Meta.model class name
        model_name = self.Meta.model.__name__
        url = f"{base_url}?model={model_name}&id={value}"
        return mark_safe(f'<a href="{url}" class="btn btn-secondary">تعديل</a>')

class DocTypeTable(tables.Table):
    edit = tables.Column(accessor='id', verbose_name='', empty_values=())

    def __init__(self, *args, model_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name

    class Meta:
        model = DocType
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'edit')
        attrs = {'class': 'table table-hover table-responsive align-middle table-sm'}

    def render_edit(self, value):
        base_url = reverse("manage_sections")
        # Derive model name from the Meta.model class name
        model_name = self.Meta.model.__name__
        url = f"{base_url}?model={model_name}&id={value}"
        return mark_safe(f'<a href="{url}" class="btn btn-secondary">تعديل</a>')


# class AffiliateTable(tables.Table):
#     subs = tables.Column(accessor='id', verbose_name='التقسيمات الفرعية', empty_values=())
#     edit = tables.Column(accessor='id', verbose_name='', empty_values=())

#     def __init__(self, *args, model_name=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.model_name = model_name

#     class Meta:
#         model = Affiliate
#         template_name = "django_tables2/bootstrap5.html"
#         fields = ('name', 'type', 'address', 'subs', 'edit')
#         attrs = {'class': 'table table-striped table-sm table align-middle'}

#     def render_edit(self, value):
#         return mark_safe(f'<a href="{reverse("manage_sections", args=[self.model_name])}?id={value}" class="btn btn-secondary">تعديل</a>')

#     def render_subs(self, value):
#         return mark_safe(f'<a href="{reverse("sub_affiliate_view", args=[value])}" class="btn btn-info">عرض</a>')


class DecreeTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name='partials/decree_actions.html',
        orderable=False,
        verbose_name=''
    )

    class Meta:
        model = Decree
        template_name = "django_tables2/bootstrap5.html"
        # List the fields you want to show in the table
        fields = ('number', 'date', 'status', 'applicant', 'company', 'country', 'ar_brand', 'en_brand', 'category', 'actions')
        attrs = {'class': 'table table-hover table-responsive align-middle'}


class PublicationTable(tables.Table):
    # Define a custom column to display the image
    img_file = tables.Column(orderable=False, verbose_name="الصورة")

    # Define actions column for edit/delete
    actions = tables.TemplateColumn(
        template_name='partials/pub_actions.html',
        orderable=False,
        verbose_name=''
    )

    # Custom method to render the image
    def render_img_file(self, value):
        if value:
            # Assuming 'value' is a file field, you can generate the URL and return the image HTML
            return mark_safe(f'<img src="{value.url}" alt="Publication Image" class="img-thumbnail" style="height: 80px; width: auto;">')
        return ''

    class Meta:
        model = Publication
        template_name = "django_tables2/bootstrap5.html"
        # List the fields you want to show in the table
        fields = ('number', 'decree', 'applicant', 'country', 'address', 'date_applied', 'category', 'img_file', 'e_number', 'created_at', 'actions')
        attrs = {'class': 'table table-hover align-middle'}


class FormPlusTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name='partials/formplus_actions.html', 
        orderable=False, 
        verbose_name=''
    )

    class Meta:
        model = FormPlus
        template_name = "django_tables2/bootstrap5.html"
        fields = ('number', 'date', 'title', 'type', 'keywords')
        attrs = {'class': 'table table-hover align-middle'}


