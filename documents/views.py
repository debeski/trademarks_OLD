
import logging
from django.contrib import messages
import os
from django.utils import timezone
from django.views import View
from django.apps import apps
import importlib
import datetime
from django.utils.safestring import mark_safe
import qrcode
import base64
from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.http import FileResponse, JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils.module_loading import import_string

import json

import mimetypes
import zipfile
from io import BytesIO

from .models import Decree, DecreeStatus, Publication, PublicationStatus, Objection, ObjectionStatus, FormPlus, Country, Government, ComType, DocType, DecreeCategory
from .genpdf import pub_pdf, obj_pdf

from django_tables2 import RequestConfig
from django.db.models import Q
import pandas as pd
import plotly.express as px

logger = logging.getLogger('documents')

def is_superuser(user):
    return user.is_superuser 

##################################################################
# Function for fetching related decrees based on a year
class DecreeAutocompleteView(View):
    def get(self, request, *args, **kwargs):
        decree_id = request.GET.get('id')  # Fetch using ID
        query = request.GET.get('q', '')
        year = request.GET.get('year', '')

        if decree_id:  # Fetch single decree by ID
            try:
                decree = Decree.objects.get(id=decree_id)
                return JsonResponse({
                    'id': decree.id,
                    'number': decree.number,
                    'date': decree.date.strftime("%Y-%m-%d") if decree.date else "",
                    'owner': decree.applicant,
                    'country': decree.country.id,
                    'date_applied': decree.date_applied.strftime("%Y-%m-%d") if decree.date_applied else "",
                    'ar_brand': decree.ar_brand,
                    'en_brand': decree.en_brand,
                    'category': decree.category.id,
                })
            except Decree.DoesNotExist:
                return JsonResponse({}, status=404)

        qs = Decree.objects.filter(status=1).exclude(deleted_at__isnull=False)
        if year:
            qs = qs.filter(date__year=year)
        if query:
            qs = qs.filter(number__icontains=query)

        results = [
            {
                'id': decree.id,
                'number': decree.number,
                'date': decree.date.strftime("%Y-%m-%d") if decree.date else "",
            }
            for decree in qs
        ]
        return JsonResponse(results, safe=False)


# Class Function for fetching related Publications based on a year
class PublicationAutocompleteView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        year = request.GET.get('year', '')
        qs = Publication.objects.filter(status=1, deleted_at__isnull=True)
        if year:
            qs = qs.filter(created_at__year=year)
        if query:
            qs = qs.filter(number__icontains=query)

        # Build a list of dictionaries for each publication
        results = [
            {
                'year': pub.year if pub.year else "",
                'number': pub.number,
                'id': pub.id,
                'decree': pub.decree.number if pub.decree else "",
                'created_at': pub.created_at.strftime("%Y-%m-%d") if pub.created_at else "",
                'applicant': pub.applicant,
                'owner': pub.owner,
                'country': pub.country.ar_name,
                'address': pub.address,
                'date_applied': pub.date_applied.strftime("%Y-%m-%d") if pub.date_applied else "",
                'ar_brand': pub.ar_brand,
                'en_brand': pub.en_brand,
                'category': pub.category.number,
                'img_file': pub.img_file.url if pub.img_file else "",
            }
            for pub in qs
        ]

        return JsonResponse(results, safe=False)


# Logger initiation Function
def log_action(action, model, object_id=None):
    timestamp = timezone.now()
    message = f"{timestamp} - Performed {action} on {model.__name__} (ID: {object_id})"
    logger.info(message)


# Function that extracts model name from a string
def get_class_from_string(class_path):
    """Dynamically imports and returns a class from a string path."""
    return import_string(class_path)


# Function for Chart generation 
def create_chart(models, start_year=2012, end_year=2025):
    """
    Generates a Plotly bar chart for document counts per year across multiple models.
    Uses caching to improve performance.
        
    :param models: List of Django models to include in the chart.
    :param start_year: Start year for filtering (default: 2008).
    :param end_year: End year for filtering (default: 2025).
    :return: HTML representation of the Plotly chart.
    """
    
    cache_key = f"chart_{start_year}_{end_year}_" + "_".join([model.__name__ for model in models])
    cached_chart = cache.get(cache_key)

    if cached_chart:
        return cached_chart  # Return cached version if available
    
    years = range(start_year, end_year + 1)
    data = []

    # Collect data from each model
    for model in models:
        model_name = model._meta.verbose_name  # Uses Django's verbose_name for readability
        for year in years:
            count = model.objects.filter(year=year, deleted_at__isnull=True).count() or 0
            data.append({'Year': year, 'Count': count, 'Model': model_name})

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Create bar chart
    fig = px.bar(
        df, x='Year', y='Count', color='Model', barmode='group',
        title='عدد الاشهارات حسب السنة',
        labels={'Model': 'النوع','Year': 'السنة', 'Count': 'عدد الاشهارات'},
        text='Count',
        hover_data={'Model': False},
    )
    
    # Update layout with hover label alignment for RTL
    fig.update_layout(
        height=340,
        title_x=0.5,
        xaxis_title='',
        yaxis_title='عدد الاشهارات',
        showlegend=False,
        autosize=True,
        margin=dict(l=40, r=20, t=40, b=0),
        font=dict(family='Shabwa, sans-serif', size=16),
        hoverlabel=dict(
            font=dict(
                family="Shabwa, sans-serif",
                size=14,
                color="white"  # For example, text color
            ),
            bgcolor="rgba(11, 27, 99, 0.9)"  # Background color if needed
        )
    )

    chart_html = fig.to_html(full_html=False)

    # Store the chart in the cache for 1 hour (3600 seconds)
    cache.set(cache_key, chart_html, timeout=3600)
    return chart_html


# Html & Chart Rendering Functions on main page only
def index(request):
    # Generate the chart HTML
    chart_html = create_chart([Publication])

    # Get the total number of publications with status 'final'
    publications = Publication.objects.filter(deleted_at__isnull=True)
    total_pub_final = publications.all().count()
    total_pub_initial = publications.filter(status=1).count()

    # Get the total number of objections with status 'pending'
    total_objections_pending = Objection.objects.filter(Q(status=1) | Q(status=2)).count()

    # Pass the values to the template context
    context = {
        'chart_html': chart_html,
        'total_pub_f': total_pub_final,
        'total_pub_i': total_pub_initial,
        'total_obj_pen': total_objections_pending
    }

    return render(request, 'index.html', context)


# Main view, and CRUD function for choice models
def core_models_view(request):
    # Read the GET parameter, defaulting to 'Country'
    model_param = request.GET.get('model', 'Country')
    
    # Mapping of model name (as string) to the actual model class
    models_map = {
        'Country': Country,
        'Government': Government,
        'ComType': ComType,
        'DocType': DocType,
        'DecreeCategory': DecreeCategory,
    }
    
    # Fallback to default if an invalid model is provided
    if model_param not in models_map:
        model_param = 'Country'
    
    selected_model = models_map[model_param]
    
    # Prepare models list with verbose names
    models_list = [
        {'name': key, 'ar_names': model._meta.verbose_name_plural}
        for key, model in models_map.items()
    ]
    
    # Get the class paths from the model
    form_class_path   = selected_model.get_form_class()
    filter_class_path = selected_model.get_filter_class()
    table_class_path  = selected_model.get_table_class()
    
    # Import the actual classes using the helper function
    FormClass   = get_class_from_string(form_class_path)
    FilterClass = get_class_from_string(filter_class_path)
    TableClass  = get_class_from_string(table_class_path)
    
    # Instantiate the objects.
    # Check if an 'id' is provided in GET parameters to edit an instance
    instance_id = request.GET.get('id')
    if instance_id:
        try:
            instance = selected_model.objects.get(pk=instance_id)
            form = FormClass(request.POST or None, instance=instance)
        except selected_model.DoesNotExist:
            form = FormClass(request.POST or None)  # Fall back to a blank form if no instance is found
    else:
        form = FormClass(request.POST or None)
    
    # For the filter, pass in the GET data and a queryset for the model.
    filter_obj = FilterClass(request.GET or None, queryset=selected_model.objects.all())
    
    # Instantiate the table from the filtered queryset.
    table = TableClass(filter_obj.qs)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            print("Form is valid and saved.")
            return redirect('manage_sections')  # Change this to your desired redirect
        else:
            print("Form is not valid. Errors:", form.errors)

    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    
    context = {
        'active_model': model_param,         # e.g., 'Country'
        'models': models_list,     # All four model names for the tabs
        'form': form,
        'filter': filter_obj,
        'table': table,
        'id': instance_id,  # Pass 'id' to the template context
        'ar_name': selected_model._meta.verbose_name,  # Add verbose_name to the context
        'ar_names': selected_model._meta.verbose_name_plural  # Add verbose_name to the context
    }
    
    return render(request, 'manage_sections.html', context)


# def generate_qr(request, sequence):
#     # Ensure the input is exactly 13 digits
#     if not sequence.isdigit() or len(sequence) != 13:
#         return HttpResponse("Invalid sequence", status=400)

#     # Generate QR code
#     qr = qrcode.make(sequence)

#     # Save QR to an in-memory buffer
#     buffer = BytesIO()
#     qr.save(buffer, format="PNG")
#     buffer.seek(0)

#     # Return QR code as an image response
#     return HttpResponse(buffer.getvalue(), content_type="image/png")


def generate_qr(sequence):
    # Ensure the input is exactly 13 digits
    if not sequence.isdigit() or len(sequence) != 13:
        raise ValueError("Invalid sequence")

    # Generate QR code
    qr = qrcode.make(sequence)

    # Save QR to an in-memory buffer
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer

def buffer_to_base64(buffer):
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# Views for Publication
#######################
# Main table view for decrees
@login_required
def decree_list(request):
    if not request.user.has_perm('documents.view_decree'):
        messages.error(request, "ليس لديك الصلاحية الكافية لزيارة هذا القسم!.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    # Get the base queryset (only non-deleted items)
    qs = Decree.objects.filter(deleted_at__isnull=True)

    # Get the status from GET parameters (None means "ALL")
    status = request.GET.get("status")
    if status is not None:
        try:
            status = int(status)
            if status in [choice[0] for choice in DecreeStatus.choices]:
                qs = qs.filter(status=status)
            else:
                status = None
        except ValueError:
            status = None

    # Dynamically import the filter class
    filter_class_path = Decree.get_filter_class()
    filter_class = get_class_from_string(filter_class_path)
    decree_filter = filter_class(request.GET, queryset=qs)

    # Dynamically import the table class
    table_class_path = Decree.get_table_class()
    table_class = get_class_from_string(table_class_path)
    table = table_class(decree_filter.qs)
    
    # Configure pagination (10 decrees per page)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    
    return render(request, 'decrees/decree_list.html', {
        'table': table,
        'filter': decree_filter,
        'current_status': status,
        'status_choices': DecreeStatus.choices,

    })


# Main Adding and Editing view for decrees
@login_required
def add_edit_decree(request, document_id=None):
    
    if not request.user.has_perm('documents.add_decree'):
        messages.error(request, "ليس لديك الصلاحية الكافية للادخال والتعديل!.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    if document_id:
        instance = get_object_or_404(Decree, id=document_id)
    else:
        instance = None

    # Dynamically import the form class
    form_class_path = Decree.get_form_class()
    form_class = get_class_from_string(form_class_path)
    form = form_class(request.POST or None, request.FILES or None, instance=instance)
    
    if request.method == 'POST' and form.is_valid():
        # Add the check here for is_placeholder field
        if instance and instance.is_placeholder:
            instance.is_placeholder = False
            instance.save()

        form.save()
        return redirect(reverse('decree_list'))

    return render(request, 'decrees/decree_form.html', {
        'form': form,
    })


# Main PDF download view for decrees
@login_required
def download_decree(request, document_id):
    """
    Downloads a decree's PDF file, attachment, or both as a ZIP file.
    """
    if not request.user.has_perm('documents.download_decree'):
        messages.error(request, "ليس لديك الصلاحية الكافية لتحميل هذا الملف!.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    decree = get_object_or_404(Decree, pk=document_id)

    # Determine file existence
    pdf_exists = decree.pdf_file and decree.pdf_file.name
    attach_exists = decree.attach and decree.attach.name

    if not pdf_exists and not attach_exists:
        return JsonResponse({'error': 'No document or attachment available for download.'}, status=404)

    # Prepare file naming
    date_str = decree.date.strftime('%Y-%m-%d') if decree.date else 'unknown_date'
    identifier = decree.number if decree.number else 'unknown'

    if pdf_exists and attach_exists:
        # Create ZIP file
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            # Add PDF to ZIP
            pdf_filename = f"decree_{identifier}_{date_str}.pdf"
            with decree.pdf_file.open('rb') as pdf_file:
                zip_file.writestr(pdf_filename, pdf_file.read())

            # Add attachment to ZIP
            attach_ext = decree.attach.name.split('.')[-1]
            attach_filename = f"decree_attachment_{identifier}_{date_str}.{attach_ext}"
            with decree.attach.open('rb') as attach_file:
                zip_file.writestr(attach_filename, attach_file.read())

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="decree_{identifier}_{date_str}.zip"'
        return response

    elif pdf_exists:
        # Download only PDF
        content_type, _ = mimetypes.guess_type(decree.pdf_file.name) or ('application/pdf',)
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="decree_{identifier}_{date_str}.pdf"'

        with decree.pdf_file.open('rb') as pdf_file:
            response.write(pdf_file.read())

        return response

    elif attach_exists:
        # Download only attachment
        content_type, _ = mimetypes.guess_type(decree.attach.name) or ('application/octet-stream',)
        attach_ext = decree.attach.name.split('.')[-1]
        attach_filename = f"decree_attachment_{identifier}_{date_str}.{attach_ext}"
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{attach_filename}"'

        with decree.attach.open('rb') as attach_file:
            response.write(attach_file.read())

        return response

    return HttpResponseNotFound('No document or attachment available for download.')


# Main soft delete view for decrees
@login_required
@user_passes_test(is_superuser)
def soft_delete_decree(request, document_id):
    """
    Soft-delete a decree by setting its deleted_at timestamp.
    """
    if request.method == 'POST':  # Change from DELETE to POST
        document = get_object_or_404(Decree, id=document_id)
        document.deleted_at = timezone.now()  # Set the deletion timestamp
        document.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# Main detail view for decrees
@login_required
def decree_detail(request, document_id):
    """
    Displays details of a decree with a PDF preview.
    """
    if not request.user.has_perm('documents.view_decree'):
        messages.error(request, "ليس لديك الصلاحية الكافية لزيارة هذا القسم!.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    decree = get_object_or_404(Decree, pk=document_id)
    return render(request, 'decrees/decree_detail.html', {'decree': decree})


# Views for Publication
#######################
# Main table view for publications
def publication_list(request):
    
    qs = Publication.objects.filter(deleted_at__isnull=True)

    # Get the status from GET parameters (None means "ALL")
    status = request.GET.get("status")
    if status is not None:
        try:
            status = int(status)
            if status in [choice[0] for choice in PublicationStatus.choices]:
                qs = qs.filter(status=status)
            else:
                status = None
        except ValueError:
            status = None

    # Dynamically import the filter class
    filter_class_path = Publication.get_filter_class()
    filter_class = get_class_from_string(filter_class_path)
    publication_filter = filter_class(request.GET, queryset=qs)

    # Dynamically import the table class
    table_class_path = Publication.get_table_class()
    table_class = get_class_from_string(table_class_path)
    table = table_class(publication_filter.qs)

    RequestConfig(request, paginate={'per_page': 20}).configure(table)

    return render(request, "publications/pub_list.html", {
        "table": table,
        "filter": publication_filter,
        "current_status": status,
        "status_choices": PublicationStatus.choices,

    })


# Main Adding and Editing view for publications
@login_required
def add_edit_publication(request, document_id=None):
    if document_id:
        instance = get_object_or_404(Publication, id=document_id)
    else:
        instance = None

    # Dynamically import the form class
    form_class_path = Publication.get_form_class()
    form_class = get_class_from_string(form_class_path)
    form = form_class(request.POST or None, request.FILES or None, instance=instance)
    
    if request.method == 'POST' and form.is_valid():
        publication = form.save()

        decree_number = form.cleaned_data['decree_number']
        selected_year = form.cleaned_data['year']  # Get the selected year from the form
        decree_owner = form.cleaned_data['owner']
        decree_country = form.cleaned_data['country']
        decree_category = form.cleaned_data['category']
        decree_date_applied = form.cleaned_data['date_applied']
        decree_ar_brand = form.cleaned_data['ar_brand']
        decree_en_brand = form.cleaned_data['en_brand']

        # Try to find an existing decree with the same number and year
        decree = Decree.objects.filter(
            number=decree_number,
            date__year=selected_year  # Use the selected year to filter the decrees
        ).first()
        
        if not decree:
            # If no matching decree found, create a new one (auto-created flag)
            decree = Decree.objects.create(
                number=decree_number,
                date=datetime.date(int(selected_year), 1, 1),
                company=decree_owner,
                country=decree_country,
                category=decree_category,
                date_applied=decree_date_applied,
                ar_brand=decree_ar_brand,
                en_brand=decree_en_brand,
                is_placeholder=True,  # Mark as auto-created
            )

        # Link the publication to the decree (ForeignKey relationship)
        publication.decree = decree
        publication.save()

        return redirect(reverse('publication_list'))

    return render(request, 'publications/pub_form.html', {
        'form': form,
    })


# Main PDF download view for publications
@login_required
def download_publication(request, document_id):
    """
    Downloads a publication's image file or attachment as a ZIP file.
    """
    publication = get_object_or_404(Publication, pk=document_id)

    # Check for image and attachment existence
    img_exists = publication.img_file and publication.img_file.name
    attach_exists = publication.attach and publication.attach.name

    if not img_exists and not attach_exists:
        return JsonResponse({'error': 'No document or attachment available for download.'}, status=404)

    # Prepare file naming
    date_str = publication.date.strftime('%Y-%m-%d') if publication.date else 'unknown_date'
    identifier = publication.number if publication.number else 'unknown'

    if img_exists and attach_exists:
        # Create ZIP file
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            # Add Image to ZIP
            img_filename = f"publication_{identifier}_{date_str}.jpg"
            with publication.img_file.open('rb') as img_file:
                zip_file.writestr(img_filename, img_file.read())

            # Add attachment to ZIP
            attach_ext = publication.attach.name.split('.')[-1]
            attach_filename = f"publication_attachment_{identifier}_{date_str}.{attach_ext}"
            with publication.attach.open('rb') as attach_file:
                zip_file.writestr(attach_filename, attach_file.read())

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="publication_{identifier}_{date_str}.zip"'
        return response

    elif img_exists:
        # Download only image
        content_type, _ = mimetypes.guess_type(publication.img_file.name) or ('image/jpeg',)
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="publication_{identifier}_{date_str}.jpg"'

        with publication.img_file.open('rb') as img_file:
            response.write(img_file.read())

        return response

    elif attach_exists:
        # Download only attachment
        content_type, _ = mimetypes.guess_type(publication.attach.name) or ('application/octet-stream',)
        attach_ext = publication.attach.name.split('.')[-1]
        attach_filename = f"publication_attachment_{identifier}_{date_str}.{attach_ext}"
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{attach_filename}"'

        with publication.attach.open('rb') as attach_file:
            response.write(attach_file.read())

        return response

    return HttpResponseNotFound('No document or attachment available for download.')


# Main soft delete view for publications
@login_required
@user_passes_test(is_superuser)
def soft_delete_publication(request, document_id):
    """
    Soft-delete a publication by setting its deleted_at timestamp.
    """
    if request.method == 'POST':  # Change from DELETE to POST
        document = get_object_or_404(Publication, id=document_id)
        document.deleted_at = timezone.now()  # Set the deletion timestamp
        document.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# Main detail view for publications
@login_required
def publication_detail(request, document_id):
    """
    Displays details of a publication with image preview.
    """
    publication = get_object_or_404(Publication, pk=document_id)

    # Fetch the decree if it exists
    decree = publication.decree

    return render(request, 'publications/pub_detail.html', {
        'publication': publication,
        'decree': decree  # Pass the decree object
    })


# Function for changing status of an intial publication to final using a button
@login_required
@permission_required('documents.can_change_status', raise_exception=True)  # Check for specific permission
def update_status(request, document_id):
    """
    Update publication status from 'initial' (1) to 'final' (3).
    """
    if request.method == 'POST':  # Handling POST request for status change
        publication = get_object_or_404(Publication, id=document_id)
        # Check if the publication is in 'initial' status
        if publication.status == 1:

            publication.status = 3
            publication.decree.is_published = True
            publication.decree.save()
            publication.save()
            messages.success(request, f"تم تغيير حالة الاشهار رقم {publication.number} إلى 'نشر نهائي'.")
        else:
            messages.error(request, "لا يمكن تغيير حالة هذه الوثيقة لأنها ليست في الحالة 'مبدئي'.")
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# Function for fetching publication data for PDF generation:
def fetch_pub_data(pub_id):
    # Fetch the import record based on trans_id
    pub_record = get_object_or_404(Publication, id=pub_id)
    # Prepare the record details
    pub_record = {
        'pub_id': pub_record.id,
        'pub_year': pub_record.year,
        'pub_date': pub_record.created_at.strftime("%d-%m-%Y"),
        'pub_no': pub_record.number,
        'dec_no': pub_record.decree.number if pub_record.decree else "N/A",
        'applicant': pub_record.applicant if pub_record.applicant else "N/A",
        'owner': pub_record.owner if pub_record.owner else "N/A",
        'country': pub_record.country.ar_name if pub_record.country else "N/A",
        'address': pub_record.address if pub_record.address else "N/A",
        'date_applied': pub_record.date_applied.strftime("%d-%m-%Y") if pub_record.date_applied else "N/A",
        'ar_brand': pub_record.ar_brand if pub_record.ar_brand else "N/A",
        'en_brand': pub_record.en_brand if pub_record.en_brand else "N/A",
        'category': pub_record.category if pub_record.category else "N/A",
        'pub_img': pub_record.img_file.url if pub_record.img_file else "N/A",
        'e_number': pub_record.e_number if pub_record.e_number else "N/A",
        'status': pub_record.status if pub_record.status else "N/A",
        'notes': pub_record.notes or "N/A",
    }

    print(f'fetched record info for Import Record No {pub_id} successfully')
    return pub_record


# Function for generating PDF for publications
@login_required
def gen_pub_pdf(request, pub_id):
    # if model == 'publication':
    record_info = fetch_pub_data(pub_id)
    pdf_data = pub_pdf(pub_id, record_info)
    # else:
    #     return HttpResponse("Invalid model type", status=400)
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pub_id}.pdf"'

    return response


# Views for Objection
#####################
# Main table view for Objection
@login_required
def objection_list(request):
    
    # Check if the user has the required permission
    if not request.user.has_perm('documents.view_objection'):
        messages.error(request, "ليس لديك الصلاحية الكافية لزيارة هذا القسم!.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    # Get the base queryset (only non-deleted items)
    qs = Objection.objects.filter(deleted_at__isnull=True)

    # Get the status from GET parameters (None means "ALL")
    status = request.GET.get("status")
    if status is not None:
        try:
            status = int(status)
            if status in [choice[0] for choice in ObjectionStatus.choices]:
                qs = qs.filter(status=status)
            else:
                status = None
        except ValueError:
            status = None

    # Get the filter class and apply it
    filter_class_path = Objection.get_filter_class()
    filter_class = get_class_from_string(filter_class_path)
    objection_filter = filter_class(request.GET, queryset=qs)
    
    # Get the table class and create the table based on the filtered queryset
    table_class_path = Objection.get_table_class()
    table_class = get_class_from_string(table_class_path)
    table = table_class(objection_filter.qs)
    
    # Configure pagination (10 objections per page)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    
    return render(request, 'objections/objection_list.html', {
        'table': table,
        'filter': objection_filter,
        'current_status': status,
        'status_choices': ObjectionStatus.choices,
    })


# Main Adding view for Objection
def add_objection(request):
    form_class = get_class_from_string(Objection.get_form_class())  # Resolving the form class

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            pub_id = form.cleaned_data.get("pub_id")  # Get the pub_id
            publication = get_object_or_404(Publication, id=pub_id, deleted_at__isnull=True)
            
            print(f"Found Publication: {publication}")  # Debugging output

            objection = form.save(commit=False)
            objection.pub = publication  # Assign the publication object, not just the ID
            objection.save()

            messages.success(request, "Objection added successfully!")
            return redirect("objection_list")

        else:
            print(form.errors)  # Debugging: Print form errors if invalid

    else:
        form = form_class(request.POST or None, request.FILES or None)

    return render(request, 'objections/objection_form.html', {'form': form})


# Main Editing view for Objection
def edit_objection(request, document_id):
    """
    Function to edit an existing objection.
    """
    form_class = get_class_from_string(Objection.get_form_class())  # Resolving the form class
    objection = get_object_or_404(Objection, id=document_id)  # Get the existing Objection object
    publication = objection.pub  # Get the associated Publication for the existing Objection

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=objection)
        if form.is_valid():
            objection.save()
            messages.success(request, "Objection updated successfully!")
            return redirect("objection_list")
        else:
            print(form.errors)  # Debugging: Print form errors if invalid

    else:
        form = form_class(instance=objection)

    return render(request, 'objections/objection_form.html', {'form': form, 'objection': objection})


def objection_pub_pick(request):
    qs = Publication.objects.filter(deleted_at__isnull=True, status=1)

    # Use the same filter logic but for status=1 only
    filter_class_path = Publication.get_filter_class()
    filter_class = get_class_from_string(filter_class_path)
    publication_filter = filter_class(request.GET, queryset=qs)

    # Use a separate table for the new page
    table_class = get_class_from_string(Publication.get_table_class(context="objection_pub_pick"))
    table = table_class(publication_filter.qs)

    RequestConfig(request, paginate={'per_page': 20}).configure(table)

    return render(request, "objections/objection_pub_pick.html", {
        "table": table,
        "filter": publication_filter,
    })


def add_pub_objection(request, document_id=None):
    """
    Function to add a new objection for a given publication for the public.
    """
    form_class = get_class_from_string(Objection.get_form_class(context="objection_pub_pick"))  # Resolving the form class
    
    if document_id:
        publication = get_object_or_404(Publication, id=document_id, deleted_at__isnull=True)  # Get the publication
        
    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            objection = form.save(commit=False)
            objection.pub = publication
            
            # Check the values of is_paid and receipt_file directly in the if statement
            if form.cleaned_data.get('is_paid') and form.cleaned_data.get('receipt_file'):
                objection.status = 2
            else:
                objection.status = 1
            objection.save()
            qr_buffer = generate_qr(objection.unique_code)
            qr_base64 = buffer_to_base64(qr_buffer)
            # Prepare the success message with the PDF link
            success_msg = f"""
                <div style="display: flex; align-items: center;">
                    <div style="flex: 1; margin-right: 10px;">
                        <p>تم تقديم الاعتراض مبدئيا.</p>
                        <p>رقمك المميز هو: <strong>{objection.unique_code}</strong></p>
                        <p>احفظه في مكان ما لكي تتمكن من مراجعة طلب اعتراضك لاحقا.</p>
                        <p>يمكنك تحميل نموذج الاعتراض <a href='{reverse('gen_obj_pdf', kwargs={'obj_id': objection.id})}' target='_blank'>من هنا</a>.</p>
                        <p>في حالة لم تقم بدفع الرسوم بعد، يرجى طباعة نموذج الاعتراض اعلاه والتوجه به الى اقرب مكان دفع.</p>
                    </div>
                    <img src='data:image/png;base64,{qr_base64}' alt='QR Code' style='width: 250px; height: auto;' />  <!-- Adjust the width as needed -->
                </div>
            """

            # Mark the message as safe to render HTML
            messages.success(request, mark_safe(success_msg))

            return redirect('index')  # Redirect to the index page
        else:
            print(form.errors)  # Debugging: Print form errors if invalid

    else:
        form = form_class()
    
    return render(request, 'objections/objection_pub_form.html', {'form': form, 'publication': publication})


# Function for fetching objection data for PDF generation
def fetch_objection_data(obj_id):
    # Fetch the objection record based on its ID
    obj_record = get_object_or_404(Objection, id=obj_id)
    
    # Prepare the record details
    objection_data = {
        'obj_id': obj_record.id,
        'obj_number': obj_record.number,
        'pub_id': obj_record.pub.id if obj_record.pub else "N/A",
        'pub_no': obj_record.pub.number if obj_record.pub else "N/A",
        'pub_year': obj_record.pub.year if obj_record.pub else "N/A",
        'applicant': obj_record.pub.applicant if obj_record.pub and obj_record.pub.applicant else "N/A",
        'owner': obj_record.pub.owner if obj_record.pub and obj_record.pub.owner else "N/A",
        'obj_date': obj_record.created_at.strftime("%d-%m-%Y"),
        'name': obj_record.name,
        'job': obj_record.job,
        'nationality': obj_record.nationality.ar_name if obj_record.nationality else "N/A",
        'address': obj_record.address,
        'phone': obj_record.phone,
        'com_name': obj_record.com_name,
        'com_job': obj_record.com_job.name if obj_record.com_job else "N/A",
        'com_address': obj_record.com_address,
        'com_og_address': obj_record.com_og_address,
        'com_mail_address': obj_record.com_mail_address,
        'status': obj_record.get_status_display(),
        'reason': obj_record.reason if obj_record.reason else "N/A",
        'is_paid': "Yes" if obj_record.is_paid else "No",
        'receipt_file': obj_record.receipt_file.url if obj_record.receipt_file else "N/A",
        'unique_code': obj_record.unique_code,
        'notes': obj_record.notes or "N/A",
    }

    print(f'Fetched record info for Objection No {obj_id} successfully')
    return objection_data


def gen_obj_pdf(request, obj_id):
    """
    Generates and returns a PDF for the specified objection.
    """
    # Fetch objection data
    obj_record = fetch_objection_data(obj_id)
    
    # Generate the PDF (assuming a `obj_pdf` function exists similar to `pub_pdf`)
    pdf_data = obj_pdf(obj_id, obj_record)

    # Return the PDF as a response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="objection_{obj_id}.pdf"'

    return response



# def add_objection(request):
#     """
#     Function to add a new objection for a given publication.
#     """
#     form_class = get_class_from_string(Objection.get_form_class())  # Resolving the form class
#     publication = get_object_or_404(Publication, id=document_id, deleted_at__isnull=True)  # Get the publication
    
#     if request.method == "POST":
#         form = form_class(request.POST, request.FILES)
#         if form.is_valid():
#             objection = form.save(commit=False)
#             objection.pub = publication  # Assign the related publication
#             objection.save()

#             messages.success(request, "Objection added successfully!")
#             return redirect("objection_list")
#         else:
#             print(form.errors)  # Debugging: Print form errors if invalid

#     else:
#         form = form_class()

#     return render(request, 'objections/objection_form.html', {'form': form, 'publication': publication})


# Main PDF download view for Objection
@login_required
def download_objection(request, document_id):
    """
    Downloads an objection's PDF file.
    """
    objection = get_object_or_404(Objection, pk=document_id)

    # Check if PDF exists
    pdf_exists = objection.pdf_file and objection.pdf_file.name

    if not pdf_exists:
        return JsonResponse({'error': 'No PDF document available for download.'}, status=404)

    # Prepare file naming
    date_str = objection.date.strftime('%Y-%m-%d') if objection.date else 'unknown_date'
    identifier = objection.number if objection.number else 'unknown'

    # Download only PDF
    content_type, _ = mimetypes.guess_type(objection.pdf_file.name) or ('application/pdf',)
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="objection_{identifier}_{date_str}.pdf"'

    with objection.pdf_file.open('rb') as pdf_file:
        response.write(pdf_file.read())

    return response


# Main soft delete view for Objection
@login_required
@user_passes_test(is_superuser)
def soft_delete_objection(request, document_id):
    """
    Soft-delete an objection by setting its deleted_at timestamp.
    """
    if request.method == 'POST':  # Change from DELETE to POST
        document = get_object_or_404(Objection, id=document_id)
        document.deleted_at = timezone.now()  # Set the deletion timestamp
        document.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# Main detail view for Objection
@login_required
def objection_detail(request, document_id):
    """
    Displays details of an objection with a PDF preview.
    """
    objection = get_object_or_404(Objection, pk=document_id)
    return render(request, 'objections/objection_detail.html', {'objection': objection})


@csrf_exempt  # Allow AJAX requests without CSRF token (only if necessary)
def check_objection_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            unique_code = data.get("unique_code")
            phone_number = data.get("phone_number")

            # Query the database for the objection
            objection = Objection.objects.filter(unique_code=unique_code, phone=phone_number).first()

            if objection:
                return JsonResponse({
                    "success": True,
                    "status": objection.get_status_display(),
                    "com_name": objection.com_name,
                    "brand": f"{objection.pub.ar_brand} - {objection.pub.en_brand} <br> الفئة: {objection.pub.category}",
                    "date": objection.created_at.strftime("%d-%m-%Y")
                })
            else:
                return JsonResponse({"success": False, "error": "لم يتم العثور على اعتراض مطابق."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "طلب غير صالح."}, status=400)


# Function for changing status of an unconfirmed objection to paid using a button
@login_required
@permission_required('documents.confirm_objection_fee', raise_exception=True)
def confirm_objection_fee(request, document_id):
    """
    Update Objection status from (unconfirm) to (paid).
    """
    if request.method == 'POST':
        objection = get_object_or_404(Objection, id=document_id)
        # Check if the objection is in 'unconfirm' status
        if objection.status == 2:

            objection.status = 3
            objection.is_paid = False
            objection.pub.status = 2
            objection.pub.save()
            objection.save()
            
            messages.success(request, f"تم تغيير حالة الاشهار رقم {objection.number} إلى 'نشر نهائي'.")
        else:
            messages.error(request, "لا يمكن تغيير حالة هذه الوثيقة لأنها ليست في الحالة 'مبدئي'.")
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# Function for changing status of an unconfirmed objection to rejected using a button
@login_required
@permission_required('documents.confirm_objection_fee', raise_exception=True)
def decline_objection_fee(request, document_id):
    """
    Update Objection status from (unconfirm) to (declined).
    """
    if request.method == 'POST':
        objection = get_object_or_404(Objection, id=document_id)
        # Check if the objection is in 'unconfirm' status
        if objection.status == 2:

            objection.status = 5
            objection.is_paid = False
            other_objections = Objection.objects.filter(pub=objection.pub).exclude(id=objection.id)
            if not other_objections.exists():
                objection.pub.status = 1  # Set the publication status to 1 if no other objections exist

            objection.pub.save()
            objection.save()
            
            messages.warning(request, f"تم تغيير حالة الاشهار رقم {objection.number} إلى 'رفض'.")
        else:
            messages.error(request, "لا يمكن تغيير حالة هذه الوثيقة لأنها ليست في الحالة 'مبدئي'.")
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# Views for FormPlus
####################
# Main table view for FormPlus
def formplus_list(request):
    # Get the base queryset (only non-deleted items)
    qs = FormPlus.objects.filter(deleted_at__isnull=True)
    
    # Dynamically import the filter class
    filter_class_path = FormPlus.get_filter_class()
    filter_class = get_class_from_string(filter_class_path)
    formplus_filter = filter_class(request.GET, queryset=qs)

    # Dynamically import the table class
    table_class_path = FormPlus.get_table_class()
    table_class = get_class_from_string(table_class_path)
    table = table_class(formplus_filter.qs)
    
    # Configure pagination (10 decrees per page)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    
    return render(request, 'formplus/formplus_list.html', {
        'table': table,
        'filter': formplus_filter,
    })


# Main Adding and Editing view for FormPlus
@login_required
def add_edit_formplus(request, document_id=None):
    instance = get_object_or_404(FormPlus, id=document_id) if document_id else None

    # Dynamically import the form class
    form_class_path = FormPlus.get_form_class()
    form_class = get_class_from_string(form_class_path)
    form = form_class(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('formplus_list'))  # Adjust URL name as needed

    return render(request, 'formplus/formplus_form.html', {'form': form})


# Main PDF download view for FormPlus
def download_formplus(request, document_id):
    """
    Downloads a FormPlus document's PDF file.
    """
    formplus = get_object_or_404(FormPlus, pk=document_id)

    # Check if the PDF file exists
    if not formplus.pdf_file or not formplus.pdf_file.name:
        return JsonResponse({'error': 'No document available for download.'}, status=404)

    # Prepare file naming
    date_str = formplus.date.strftime('%Y-%m-%d') if formplus.date else 'unknown_date'
    identifier = formplus.number if formplus.number else 'unknown'
    pdf_filename = f"formplus_{identifier}_{date_str}.pdf"

    # Set content type and response
    content_type, _ = mimetypes.guess_type(formplus.pdf_file.name) or ('application/pdf',)
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'

    # Serve the PDF file
    with formplus.pdf_file.open('rb') as pdf_file:
        response.write(pdf_file.read())

    return response


# Main soft delete view for FormPlus
@login_required
@user_passes_test(is_superuser)
def soft_delete_formplus(request, document_id):
    """
    Soft-delete a FormPlus document by setting its deleted_at timestamp.
    """
    if request.method == 'POST':  # Change from DELETE to POST
        document = get_object_or_404(FormPlus, id=document_id)
        document.deleted_at = timezone.now()  # Set the deletion timestamp
        document.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# Main detail view for FormPlus
def formplus_detail(request, document_id):
    """
    Displays details of a FormPlus document with a PDF preview.
    """
    formplus = get_object_or_404(FormPlus, pk=document_id)
    return render(request, 'formplus/formplus_detail.html', {'formplus': formplus})


