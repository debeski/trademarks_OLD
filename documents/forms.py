from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, Div, HTML
from crispy_forms.bootstrap import FormActions
from .models import Decree, Publication, FormPlus, Objection, Country, Government, ComType, DocType

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['en_name', 'ar_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Div(Field('en_name', css_class='form-control', placeholder="الاسم بالانجليزية"), css_class='col-md-5'),
                Div(Field('ar_name', css_class='form-control', placeholder="الاسم بالعربية"), css_class='col-md-5'),
                FormActions(
                    Submit('submit', '{% if id %} حفظ {% else %} اضافة جديد {% endif %}', css_class='btn btn-primary'),
                    HTML(
                        '{% if id %}'
                        ' <a class="btn btn-secondary" href="{% url "manage_sections" %}">الغاء</a>'
                        '{% endif %}'
                    ), css_class='col-md-auto'
                )
            ),
        )

class GovernmentForm(forms.ModelForm):
    class Meta:
        model = Government
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Row(
                Div(Field('name', css_class='form-control', placeholder="اسم النوع"), css_class='col-md-10'),
                FormActions(
                    Submit('submit', '{% if id %} حفظ {% else %} اضافة جديد {% endif %}', css_class='btn btn-primary'),
                    HTML(
                        '{% if id %}'
                        ' <a class="btn btn-secondary" href="{% url "manage_sections" %}">الغاء</a>'
                        '{% endif %}'
                    ), css_class='col-md-auto'
                )
            ),
        )

class ComTypeForm(forms.ModelForm):
    class Meta:
        model = ComType
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Row(
                Div(Field('name', css_class='form-control', placeholder="اسم النوع"), css_class='col-md-10'),
                FormActions(
                    Submit('submit', '{% if id %} حفظ {% else %} اضافة جديد {% endif %}', css_class='btn btn-primary'),
                    HTML(
                        '{% if id %}'
                        ' <a class="btn btn-secondary" href="{% url "manage_sections" %}">الغاء</a>'
                        '{% endif %}'
                    ), css_class='col-md-auto'
                )
            ),
        )

class DocTypeForm(forms.ModelForm):
    class Meta:
        model = DocType
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Row(
                Div(Field('name', css_class='form-control', placeholder="اسم النوع"), css_class='col-md-10'),
                FormActions(
                    Submit('submit', '{% if id %} حفظ {% else %} اضافة جديد {% endif %}', css_class='btn btn-primary'),
                    HTML(
                        '{% if id %}'
                        ' <a class="btn btn-secondary" href="{% url "manage_sections" %}">الغاء</a>'
                        '{% endif %}'
                    ), css_class='col-md-auto'
                )
            ),
        )


class DecreeForm(forms.ModelForm):
    class Meta:
        model = Decree
        # List the fields you want to include (adjust as needed)
        fields = [
            'number', 'date', 'status', 'applicant', 'company', 'country',
            'date_applied', 'number_applied', 'ar_brand', 'en_brand',
            'category', 'pdf_file', 'attach', 'notes'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize the crispy helper
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.form_class = 'w-75 mx-auto'
        self.fields['status'].empty_label = None
        # Define a layout for the fields.
        self.helper.layout = Layout(
            Div(
                Div(Field('number', css_class='form-control'), css_class='col'),
                Div(Field('date', css_class='form-control flatpickr'), css_class='col'),
                Div(Field('status', css_class='form-control'), css_class='col'),
                Div(Field('applicant', css_class='form-control'), css_class='col'),
                Div(Field('company', css_class='form-control'), css_class='col'),
                Div(Field('country', css_class='form-control'), css_class='col'),
                Div(Field('date_applied', css_class='form-control flatpickr'), css_class='col'),
                Div(Field('number_applied', css_class='form-control'), css_class='col'),
                Div(Field('ar_brand', css_class='form-control'), css_class='col'),
                Div(Field('en_brand', css_class='form-control'), css_class='col'),
                Div(Field('category', css_class='form-control'), css_class='col'),
                css_class='col'
            ),
            Field('pdf_file'),
            Field('attach'),
            Field('notes', rows="2"),
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a class="btn btn-secondary" href="{% url \'decree_list\' %}">إلغاء</a>')
            )
        )


def get_decree_year_choices():
    # Get distinct years where status is 'accepted'
    years = (
        Decree.objects.filter(status="accepted")
        .values_list('date__year', flat=True)
        .distinct()
        .order_by('date__year')
    )
    return [(year, year) for year in years if year]  # Ensure no None values

def get_accepted_decrees_by_year(year=None):
    """
    Fetch decrees that have status='accepted' and optionally filter by a given year.
    """
    queryset = Decree.objects.filter(status='accepted')

    if year:
        queryset = queryset.filter(date__year=year)

    return queryset.values_list('number', flat=True)  # Only return decree numbers


class PublicationForm(forms.ModelForm):
    # Extra field to filter decrees by year
    year = forms.CharField(required=False, label="سنة القرار")
    # For the decree field, we use a ModelChoiceField; its widget will be enhanced by JavaScript.
    decree = forms.CharField(
        required=False,
        label="رقم القرار",
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'id': 'id_decree_autocomplete'})
    )

    class Meta:
        model = Publication
        fields = [
            'year', 'number', 'decree',
            'applicant', 'owner', 'country',
            'address', 'date_applied',
            'ar_brand', 'en_brand', 'category',
            'img_file', 'attach', 'e_number',
            'status', 'is_hidden', 'notes'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark fields that will be auto-filled as read-only.
        # for field_name in ['owner', 'country', 'ar_brand', 'en_brand', 'category']:
        #     self.fields[field_name].widget.attrs.update({'readonly': 'readonly', 'class': 'auto-fill'})
        # Setup crispy helper.
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Div(Field('year', css_class='form-control'), css_class='col-md-3'),
                Div(Field('decree', css_class='form-control', placeholder="اكتب رقم القرار للبحث"), css_class='col-md-9'),
                css_class='form-row'
            ),
            HTML("<hr>"),
            Div(
                Div(Field('number', css_class='form-control'), css_class='col'),
                Div(Field('applicant', css_class='form-control'), css_class='col'),
                Div(Field('owner', css_class='form-control'), css_class='col'),
                Div(Field('country', css_class='form-control'), css_class='col'),
                Div(Field('address', css_class='form-control'), css_class='col'),
                Div(Field('date_applied', css_class='form-control'), css_class='col'),
                Div(Field('ar_brand', css_class='form-control'), css_class='col'),
                Div(Field('en_brand', css_class='form-control'), css_class='col'),
                Div(Field('category', css_class='form-control'), css_class='col'),
                css_class='col'
            ),
            Field('img_file'),
            Field('attach'),
            Div(
                Div(Field('e_number', css_class='form-control'), css_class='col'),
                Div(Field('status', css_class='form-control'), css_class='col'),
                Div(Field('notes', css_class='form-control', rows="2"), css_class='col'),
                css_class='col'
            ),

            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a class="btn btn-secondary" href="{% url \'publication_list\' %}">إلغاء</a>')
            )
        )


class FormPlusForm(forms.ModelForm):
    class Meta:
        model = FormPlus
        fields = ['type', 'number', 'date', 'title', 'keywords', 'pdf_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.form_class = 'w-75 mx-auto'

        self.helper.layout = Layout(
            Div(
                Div(Field('type', css_class='form-control'), css_class='col'),
                Div(Field('number', css_class='form-control'), css_class='col'),
                Div(Field('date', css_class='form-control flatpickr'), css_class='col'),
                Div(Field('title', css_class='form-control'), css_class='col'),
                Div(Field('keywords', css_class='form-control'), css_class='col'),
                css_class='col'
            ),
            Field('pdf_file'),
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a class="btn btn-secondary" href="{% url \'formplus_list\' %}">إلغاء</a>')
            )
        )