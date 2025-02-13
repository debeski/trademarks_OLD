from django import forms
import django_filters
from django_filters.widgets import BooleanWidget
from django.forms.widgets import TextInput
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, HTML, Div
from .models import Decree, Publication, FormPlus, Objection, Country, Government, ComType, DocType


# Function to rename first choice in selection menu
def set_first_choice(field, placeholder):
    """Set the first choice of a specified select field."""
    if hasattr(field, 'choices'):
        field.empty_label = placeholder


class CountryFilter(django_filters.FilterSet):

    keyword = django_filters.CharFilter(
        method='filter_keyword',
        label='',
    )

    class Meta:
        model = Country
        fields = ['en_name', 'ar_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = 'GET'
        self.form.helper.form_class = 'form-inline'
        self.form.helper.form_show_labels = False
        self.form.helper.layout = Layout(
            Row(
                Column(Field('keyword', placeholder="البحث"), css_class='form-group col-md-6'),
                Column(Submit('submit', 'بحث', css_class='btn btn-secondary w-100'), css_class='form-group col-md-auto text-center'),
                Column(HTML('{% if request.GET and request.GET.keys|length > 2 %} <a href="{% url "manage_sections" %}" class="btn btn-warning">clear</a> {% endif %}'), css_class='form-group col-md-auto text-center'),
                css_class='form-row'
            ),
        )

    def filter_keyword(self, queryset, name, value):
        """
        Filter the queryset by matching the keyword in number, applicant, company,
        and, if applicable, the year extracted from the date field.
        """
        q = Q(en_name__icontains=value) | Q(ar_name__icontains=value)
        return queryset.filter(q)


class GovernmentFilter(django_filters.FilterSet):
    
    class Meta:
        model = Government
        fields = {
            'name': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = 'GET'
        self.form.helper.form_class = 'form-inline'
        self.form.helper.form_show_labels = False
        self.form.helper.layout = Layout(
            Row(
                Column(Field('name__icontains', placeholder="البحث"), css_class='form-group col-md-6'),
                Column(Submit('submit', 'بحث', css_class='btn btn-secondary w-100'), css_class='form-group col-md-auto text-center'),
                Column(HTML('{% if request.GET and request.GET.keys|length > 2 %} <a href="{% url "manage_sections" %}" class="btn btn-warning">clear</a> {% endif %}'), css_class='form-group col-md-auto text-center'),
                css_class='form-row'
            ),
        )

class ComTypeFilter(django_filters.FilterSet):
    
    class Meta:
        model = ComType
        fields = {
            'name': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = 'GET'
        self.form.helper.form_class = 'form-inline'
        self.form.helper.form_show_labels = False
        self.form.helper.layout = Layout(
            Row(
                Column(Field('name__icontains', placeholder="البحث"), css_class='form-group col-md-6'),
                Column(Submit('submit', 'بحث', css_class='btn btn-secondary w-100'), css_class='form-group col-md-auto text-center'),
                Column(HTML('{% if request.GET and request.GET.keys|length > 2 %} <a href="{% url "manage_sections" %}" class="btn btn-warning">clear</a> {% endif %}'), css_class='form-group col-md-auto text-center'),
                css_class='form-row'
            ),
        )

class DocTypeFilter(django_filters.FilterSet):
    
    class Meta:
        model = DocType
        fields = {
            'name': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = 'GET'
        self.form.helper.form_class = 'form-inline'
        self.form.helper.form_show_labels = False
        self.form.helper.layout = Layout(
            Row(
                Column(Field('name__icontains', placeholder="البحث"), css_class='form-group col-md-6'),
                Column(Submit('submit', 'بحث', css_class='btn btn-secondary w-100'), css_class='form-group col-md-auto text-center'),
                Column(HTML('{% if request.GET and request.GET.keys|length > 2 %} <a href="{% url "manage_sections" %}" class="btn btn-warning">clear</a> {% endif %}'), css_class='form-group col-md-auto text-center'),
                css_class='form-row'
            ),
        )


class DecreeFilter(django_filters.FilterSet):

    keyword = django_filters.CharFilter(
        method='filter_keyword',
        label='',
    )
    
    date__year = django_filters.NumberFilter(
        field_name="date__year",
        lookup_expr="exact",
        widget=forms.NumberInput(attrs={'min': 2000, 'max': 2025, 'placeholder': 'السنة'}),
    )
    
    class Meta:
        model = Decree
        fields = {
            'status': ['exact'],
            'country': ['exact'],
            'date': ['gte', 'lte'],
            'date_applied': ['gte', 'lte'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_first_choice(self.filters['status'].field, 'حالة الطلب')
        set_first_choice(self.filters['country'].field, 'الدولة')
        self.form.helper = FormHelper()
        self.form.helper.form_method = 'GET'
        self.form.helper.form_class = 'form-inline'
        self.form.helper.form_show_labels = False
        self.form.helper.layout = Layout(
            # Keyword search (Always visible)
            Row(
                Column(HTML('{% if request.user.is_authenticated %} <a href="{% url "add_decree" %}" class="btn btn-primary active w-100"><i class="bi bi-plus-lg"></i> إضافة جديد</a> {% endif %}'), css_class='col-md-auto text-center'),
                Column(Field('keyword', placeholder="البحث (رقم، مقدم الطلب، صاحب العلامة)"), css_class='form-group col-md-6'),
                Column(Submit('submit', 'بحث', css_class='btn btn-secondary w-100'), css_class='form-group col-md-auto text-center'),
                Column(HTML('<button class="btn btn-outline-secondary w-100" type="button" data-bs-toggle="collapse" data-bs-target="#advanced-search">بحث متقدم</button>'), css_class='form-group col-md-auto text-center'),
                Column(HTML('{% if request.GET %} <a href="{% url "decree_list" %}" class="btn btn-warning">clear</a> {% endif %}'), css_class='form-group col-md-auto text-center'),
                css_class='form-row'
            ),
            
            # Advanced filters (Initially hidden, expands on button click)
            Div(
                Row(
                    Column(Field('status', placeholder="الحالة"), css_class='form-group col-md-2'),
                    Column(Field('country', placeholder="الدولة"), css_class='form-group col-md-2'),
                    Column(Field('date__year', placeholder="السنة", dir="rtl"), css_class='form-group col-md-2'),
                    
                    Column(HTML("<strong>تاريخ القرار</strong>"), css_class='col-md-1 text-center align-self-center mb-3'),
                    Column(Field('date__gte', css_class='flatpickr', placeholder="من "), css_class='form-group col-md-1'),
                    Column(Field('date__lte', css_class='flatpickr', placeholder="إلى "), css_class='form-group col-md-1'),
                    
                    Column(HTML("<strong>تاريخ التقديم</strong>"), css_class='col-md-1 text-center align-self-center mb-3'),
                    Column(Field('date_applied__gte', css_class='flatpickr', placeholder="من "), css_class='form-group col-md-1'),
                    Column(Field('date_applied__lte', css_class='flatpickr', placeholder="إلى "), css_class='form-group col-md-1'),
                    
                    css_class='form-row mt-2 align-items-center'
                ),
                css_class="collapse mt-3",  # Bootstrap collapse class
                id="advanced-search"
            ),
        )

    def filter_keyword(self, queryset, name, value):
        """
        Filter the queryset by matching the keyword in number, applicant, company,
        and, if applicable, the year extracted from the date field.
        """
        q = Q(number__icontains=value) | Q(applicant__icontains=value) | Q(company__icontains=value)
        if value.isdigit():
            try:
                year = int(value)
                q |= Q(date__year=year)
            except ValueError:
                pass
        return queryset.filter(q)


class PublicationFilter(django_filters.FilterSet):
    
    keyword = django_filters.CharFilter(
        method='filter_keyword',
        label='',
    )
    
    date_applied__year = django_filters.NumberFilter(
        field_name="date__year",
        lookup_expr="exact",
        widget=forms.NumberInput(attrs={'min': 2000, 'max': 2025, 'placeholder': 'السنة'}),
    )
    
    class Meta:
        model = Publication
        fields = {
            'number': ['exact'],
            'status': ['exact'],
            'country': ['exact'],
            'date_applied': ['gte', 'lte'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Replace default "------" for the select fields
        set_first_choice(self.filters['country'].field, 'الدولة')
        
        # Initialize Crispy Forms helper
        self.form.helper = FormHelper()
        self.form.helper.form_method = 'GET'
        self.form.helper.form_class = 'form-inline'
        self.form.helper.form_show_labels = False

        self.form.helper.layout = Layout(
            # Row 1: Keyword search (always visible) plus Add button and basic controls.
            Row(
                Column(HTML('{% if request.user.is_authenticated %} <a href="{% url "add_publication" %}" class="btn btn-primary active w-100"><i class="bi bi-plus-lg"></i> إضافة جديد</a> {% endif %}'), css_class='col-md-auto text-center'),
                Column(Field('keyword', placeholder="البحث ( رقم، سنة، مقدم طلب، صاحب علامة.. )"), css_class='form-group col-md-6'),
                Column(Submit('submit', 'بحث', css_class='btn btn-secondary w-100'), css_class='form-group col-md-auto text-center'),
                Column(HTML('<button class="btn btn-outline-secondary w-100" type="button" data-bs-toggle="collapse" data-bs-target="#advanced-search">بحث متقدم</button>'), css_class='form-group col-md-auto text-center'),
                Column(HTML('{% if request.GET and request.GET.keys|length > 1 %} <a href="{% url "publication_list" %}?status={{ current_status }}" class="btn btn-warning">clear</a> {% endif %}'), css_class='form-group col-md-auto text-center'),
                css_class='form-row'
            ),
            # Advanced filters (hidden by default)
            Div(
                Row(
                    Column(Field('number', placeholder="رقم النشر", dir="rtl"), css_class='form-group col-md-3'),
                    Column(Field('country', placeholder="الدولة"), css_class='form-group col-md-3'),
                    Column(Field('date_applied__year', placeholder="السنة", dir="rtl"), css_class='form-group col-md-2'),
                    Column(Field('date_applied__gte', css_class='flatpickr', placeholder="من تاريخ"), css_class='form-group col-md-2'),
                    Column(Field('date_applied__lte', css_class='flatpickr', placeholder="إلى تاريخ"), css_class='form-group col-md-2'),
                    css_class='form-row mt-2 align-items-center'
                ),
                css_class="collapse mt-3",  # Bootstrap collapse class
                id="advanced-search"
            ),
            Field('status', type='hidden', value='initial')
        )


    def filter_keyword(self, queryset, name, value):
        """
        Filter the queryset by matching the keyword in number, applicant, or company,
        and if the value is numeric, also match the publication submission year.
        """
        q = Q(number__icontains=value) | Q(decree__icontains=value) | Q(applicant__icontains=value) | Q(owner__icontains=value)
        if value.isdigit():
            try:
                year = int(value)
                q |= Q(date_applied__year=year)
            except ValueError:
                pass
        return queryset.filter(q)


class FormPlusFilter(django_filters.FilterSet):

    keyword = django_filters.CharFilter(
        method='filter_keyword',
        label='',
    )
    
    date__year = django_filters.NumberFilter(
        field_name="date__year",
        lookup_expr="exact",
        widget=forms.NumberInput(attrs={'min': 2000, 'max': 2025, 'placeholder': 'السنة'}),
    )

    class Meta:
        model = FormPlus
        fields = {
            'type': ['exact'],
            'date': ['gte', 'lte'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_first_choice(self.filters['type'].field, 'نوع المستند')

        # Initialize a Crispy Forms helper for the filter form.
        self.form.helper = FormHelper()
        self.form.helper.form_method = 'GET'
        self.form.helper.form_class = 'form-inline'
        self.form.helper.form_show_labels = False  # Disable default labels

        self.form.helper.layout = Layout(
            # Keyword search (Always visible)
            Row(
                Column(HTML('{% if request.user.is_authenticated %} <a href="{% url "add_formplus" %}" class="btn btn-primary active w-100"><i class="bi bi-plus-lg"></i> إضافة جديد</a> {% endif %}'), css_class='col-md-auto text-center'),
                Column(Field('keyword', placeholder="البحث (رقم، عنوان)"), css_class='form-group col-md-6'),
                Column(Submit('submit', 'بحث', css_class='btn btn-secondary w-100'), css_class='form-group col-md-auto text-center'),
                Column(HTML('<button class="btn btn-outline-secondary w-100" type="button" data-bs-toggle="collapse" data-bs-target="#advanced-search">بحث متقدم</button>'), css_class='form-group col-md-auto text-center'),
                Column(HTML('{% if request.GET %} <a href="{% url "formplus_list" %}" class="btn btn-warning">clear</a> {% endif %}'), css_class='form-group col-md-auto text-center'),
                css_class='form-row'
            ),
            
            # Advanced filters (Initially hidden, expands on button click)
            Div(
                Row(
                    Column(Field('type', placeholder="السنة", dir="rtl"), css_class='form-group col-md-2'),
                    Column(Field('date__year', placeholder="السنة", dir="rtl"), css_class='form-group col-md-2'),
                    Column(HTML("<strong>تاريخ التقرير</strong>"), css_class='col-md-1 text-center align-self-center mb-3'),
                    Column(Field('date__gte', css_class='flatpickr', placeholder="من "), css_class='form-group col-md-1'),
                    Column(Field('date__lte', css_class='flatpickr', placeholder="إلى "), css_class='form-group col-md-1'),
                    
                    css_class='form-row mt-2 align-items-center'
                ),
                css_class="collapse mt-3",  # Bootstrap collapse class
                id="advanced-search"
            ),
        )

    def filter_keyword(self, queryset, name, value):
        """
        Filter the queryset by matching the keyword in number and title.
        """
        q = Q(number__icontains=value) | Q(title__icontains=value)
        if value.isdigit():
            try:
                year = int(value)
                q |= Q(date__year=year)
            except ValueError:
                pass
        return queryset.filter(q)