# filters.py
import django_filters
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, HTML, Div
from .models import Decree, Publication
from django.urls import reverse_lazy



# Function to rename first choice in selection menu
def set_first_choice(field, placeholder):
    """Set the first choice of a specified select field."""
    if hasattr(field, 'choices'):  # Ensure field has choices
        field.empty_label = placeholder  # Override default "------" label

add_decree_url = reverse_lazy('add_decree')  # Get URL dynamically

class DecreeFilter(django_filters.FilterSet):
    # A custom filter for keyword search across multiple fields:
    keyword_search = django_filters.CharFilter(
        method='filter_keyword',
        label='',  # Remove label
    )

    class Meta:
        model = Decree
        fields = {
            'status': ['exact'],
            'country': ['exact'],
            'date': ['year', 'gte', 'lte'],
            'date_applied': ['gte', 'lte'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the correct replacement of "------"
        set_first_choice(self.filters['status'].field, 'حالة الطلب')
        set_first_choice(self.filters['country'].field, 'الدولة')
        # Initialize a Crispy Forms helper for the filter form.
        self.form.helper = FormHelper()
        self.form.helper.form_method = 'GET'
        self.form.helper.form_class = 'form-inline'
        self.form.helper.form_show_labels = False  # Disable default labels

        self.form.helper.layout = Layout(
            # Keyword search (Always visible)
            Row(
                Column(HTML(f'<a href="{add_decree_url}" class="btn btn-primary active w-100"><i class="bi bi-plus"></i> إضافة جديد</a>'), css_class='col-md-auto text-center'),
                Column(Field('keyword_search', placeholder="البحث (رقم، مقدم الطلب، صاحب العلامة)"), css_class='form-group col-md-6'),
                Column(Submit('submit', 'بحث', css_class='btn btn-secondary w-100'), css_class='form-group col-md-auto text-center'),
                Column(HTML('<button class="btn btn-outline-secondary w-100" type="button" data-bs-toggle="collapse" data-bs-target="#advanced-search">بحث متقدم</button>'), css_class='form-group col-md-auto text-center'),
                css_class='form-row'
            ),
            
            # Advanced filters (Initially hidden, expands on button click)
            Div(
                Row(
                    Column(Field('status', placeholder="الحالة"), css_class='form-group col-md-2'),
                    Column(Field('country', placeholder="الدولة"), css_class='form-group col-md-2'),
                    Column(Field('date__year', placeholder="السنة"), css_class='form-group col-md-2'),
                    
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


# URL to add a new publication
add_publication_url = reverse_lazy('add_publication')  # Make sure your URL name is 'add_publication'

class PublicationFilter(django_filters.FilterSet):
    # A custom filter for keyword search across multiple fields:
    keyword_search = django_filters.CharFilter(
        method='filter_keyword',
        label='',  # Remove label
    )

    class Meta:
        model = Publication
        fields = {
            'status': ['exact'],
            'country': ['exact'],
            'date_applied': ['year', 'gte', 'lte'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Replace default "------" for the select fields
        set_first_choice(self.filters['status'].field, 'حالة التسجيل')
        set_first_choice(self.filters['country'].field, 'الدولة')
        # Initialize Crispy Forms helper
        self.form.helper = FormHelper()
        self.form.helper.form_method = 'GET'
        self.form.helper.form_class = 'form-inline'
        self.form.helper.form_show_labels = False

        self.form.helper.layout = Layout(
            # Row 1: Keyword search (always visible) plus Add button and basic controls.
            Row(
                Column(HTML(f'<a href="{add_publication_url}" class="btn btn-primary active w-100"><i class="bi bi-plus"></i> إضافة جديد</a>'), css_class='col-md-auto text-center'),
                Column(Field('keyword_search', placeholder="البحث (رقم، مقدم الطلب، صاحب العلامة)"), css_class='form-group col-md-6'),
                Column(Submit('submit', 'بحث', css_class='btn btn-secondary w-100'), css_class='form-group col-md-auto text-center'),
                Column(HTML('<button class="btn btn-outline-secondary w-100" type="button" data-bs-toggle="collapse" data-bs-target="#advanced-search">بحث متقدم</button>'), css_class='form-group col-md-auto text-center'),
                css_class='form-row'
            ),
            # Advanced filters (hidden by default)
            Div(
                Row(
                    Column(Field('status', placeholder="الحالة"), css_class='form-group col-md-3'),
                    Column(Field('country', placeholder="الدولة"), css_class='form-group col-md-3'),
                    Column(Field('date_applied__year', placeholder="السنة"), css_class='form-group col-md-3'),
                    Column(Field('date_applied__gte', css_class='flatpickr', placeholder="من تاريخ"), css_class='form-group col-md-1'),
                    Column(Field('date_applied__lte', css_class='flatpickr', placeholder="إلى تاريخ"), css_class='form-group col-md-1'),
                    css_class='form-row mt-2 align-items-center'
                ),
                css_class="collapse mt-3",  # Bootstrap collapse class
                id="advanced-search"
            ),
        )

    def filter_keyword(self, queryset, name, value):
        """
        Filter the queryset by matching the keyword in number, applicant, or company,
        and if the value is numeric, also match the publication submission year.
        """
        q = Q(number__icontains=value) | Q(applicant__icontains=value) | Q(company__icontains=value)
        if value.isdigit():
            try:
                year = int(value)
                q |= Q(date_applied__year=year)
            except ValueError:
                pass
        return queryset.filter(q)


