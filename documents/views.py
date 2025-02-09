
import logging
import os
from django.utils import timezone
from django.views import View

from django.shortcuts import get_object_or_404
from django.http import FileResponse, JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json

import mimetypes
import zipfile
from io import BytesIO

from .models import Decree, Publication
from .tables import DecreeTable, PublicationTable
from .filters import DecreeFilter, PublicationFilter
from .forms import DecreeForm, PublicationForm
from .genpdf import pub_pdf

from django_tables2 import RequestConfig
from django.db.models import Q
logger = logging.getLogger('documents')
##################################################################


# Logger initiation Function:
def log_action(action, model, object_id=None):
    timestamp = timezone.now()
    message = f"{timestamp} - Performed {action} on {model.__name__} (ID: {object_id})"
    logger.info(message)


# # Function to create Chart for index:
# def create_chart():
#     # Define model names
#     model_classes = [Outgoing, Incoming, Internal, Decree, Report]
#     years = range(2008, 2025)
#     data = []

#     # Fetch counts and Arabic names using get_model_name
#     for model in model_classes:
#         arabic_name = model().get_model_name

#         # Count documents for each year
#         for year in years:
#             count = model.objects.filter(date__year=year, deleted_at__isnull=True).count() or 0
#             data.append({'Year': year, 'Count': count, 'Model': arabic_name})

#     # Create a DataFrame from the data
#     df = pd.DataFrame(data)

#     # Create a Plotly Express bar chart
#     fig = px.bar(
#         df,
#         x='Year',
#         y='Count',
#         color='Model',
#         barmode='group',
#         title='عدد الوثائق حسب السنة',
#         labels={'Year': 'السنة', 'Count': 'عدد الوثائق'},
#         text='Count',
#         hover_name='Model',
#         hover_data={'Model':False}
#     )

#     # Update layout for RTL
#     fig.update_layout(
#         selectdirection='h',
#         height=370,
#         title=dict(font=dict(size=30), automargin=True),
#         title_x=0.55,  # Center the title
#         xaxis_title='',
#         yaxis_title='عدد الوثائق',

#         legend=dict(
#             orientation='h',
#             x=0.5,
#             xanchor='center',
#             y=-0,
#             yanchor='bottom'
#         ),
#         hoverlabel=dict(
#             align='right',  # Align hover text to the right
#             bgcolor='rgba(255, 255, 255, 0.8)',  # Background color
#             bordercolor='black',  # Border color
#             font=dict(size=14, color='black')  # Font settings
#         ),
#         autosize=True,  # Enable autosizing
#         margin=dict(l=50, r=50, t=40, b=0),  # Set margins
#         font=dict(family='Shabwa, sans-serif', size=16, color='black'),  # Font settings
#     )

#     # Convert the figure to HTML and include the dynamic hover label script
#     chart_html = fig.to_html(full_html=False)
#     # JavaScript for dynamic hover label positioning
#     dynamic_hover_script = """
#     <script>
#         const myDiv = document.getElementById('myDiv');
#         myDiv.on('plotly_hover', function(eventData) {
#             const hoverLabel = document.querySelector('.hovertext'); // Select the hover label
#             if (hoverLabel) {
#                 const mouseX = eventData.event.clientX; // Get mouse X position
#                 const mouseY = eventData.event.clientY; // Get mouse Y position

#                 // Adjust hover label position
#                 hoverLabel.style.left = `${mouseX + 30}px`; // Add small offset
#                 hoverLabel.style.top = `${mouseY + 40}px`;  // Add small offset
#             }
#         });
#     </script>
#     """

#     return chart_html + dynamic_hover_script


# Html & Chart Rendering Functions on main page only:
@login_required
def index(request):
    # # Generate the chart HTML
    # chart_html = create_chart()  # Get the chart HTML

    # # Define model names based on the mapping in get_model_data
    # model_names = ['incoming', 'outgoing', 'internal', 'decree', 'report']
    
    # latest_documents = []

    # for model_name in model_names:
    #     model, _, _, _, _ = get_model_data(model_name)
    #     latest_documents += list(model.objects.order_by('-created_at')[:5])

    # # Limit to the latest 5 documents across all models
    # latest_documents = sorted(latest_documents, key=lambda x: x.created_at, reverse=True)[:5]

    return render(request, 'base.html')


# # Function for Sections Management:
# def manage_sections(request, model_name):
#     current_tab = request.GET.get('tab', model_name)

#     # Fetch model, form class, arabic name, and arabic names
#     model, form_class, arabic_name, arabic_names, _ = get_model_data(current_tab)

#     # Wrap arabic_name in a dictionary if it’s a string
#     if isinstance(arabic_name, str):
#         arabic_name = {current_tab: arabic_name}

#     # Handle document editing
#     document_id = request.GET.get('id')
#     form = form_class(request.POST or None, instance=get_object_or_404(model, id=document_id) if document_id else None)

#     # Handle form submission
#     if request.method == 'POST' and form.is_valid():
#         form.save()  # This will handle saving the many-to-many relationships
#         return redirect('manage_sections', model_name=current_tab)

#     # Fetch items for the current tab's model with pagination
#     items = model.objects.all()
#     paginator = Paginator(items, 10)
#     page_number = request.GET.get(f'{current_tab}_page', 1)  # Use current_tab for pagination
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'manage_sections.html', {
#         'models': [
#             {'name': 'departments', 'form': DepartmentForm(), 'items': Department.objects.all()},
#             {'name': 'affiliates', 'form': AffiliateForm(), 'items': Affiliate.objects.all()},
#             {'name': 'ministers', 'form': MinisterForm(), 'items': Minister.objects.all()},
#             {'name': 'governments', 'form': GovernmentForm(), 'items': Government.objects.all()},
#         ],
#         'current_tab': current_tab,
#         'form': form,
#         'page_obj': page_obj,
#         'request': request,
#         'arabic_name': arabic_name,
#         'arabic_names': arabic_names,  # Ensure this is a dictionary
#         f'{current_tab}_page': page_number,  # Use current_tab for pagination
#         'arabic_name_value': arabic_name.get(current_tab, 'اسم غير معروف')
#     })


# Function for fetching related decrees based on a year:
class DecreeAutocompleteView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        year = request.GET.get('year', '')
        qs = Decree.objects.filter(status='accepted').exclude(deleted_at__isnull=False)
        if year:
            qs = qs.filter(date__year=year)
        if query:
            qs = qs.filter(number__icontains=query)
        # Build a list of dictionaries for each decree
        results = []
        for decree in qs:
            results.append({
                'id': decree.id,
                'number': decree.number,
                'date': decree.date.strftime("%Y-%m-%d") if decree.date else "",
                'owner': decree.applicant,
                'country': decree.country,
                'date_applied': decree.date_applied.strftime("%Y-%m-%d") if decree.date_applied else "",
                'ar_brand': decree.ar_brand,
                'en_brand': decree.en_brand,
                'category': decree.category,
            })
        return JsonResponse(results, safe=False)


# Main table view for decrees
@login_required
def decree_list(request):
    # Get the base queryset (only non-deleted items)
    qs = Decree.objects.filter(deleted_at__isnull=True)
    
    # Apply django-filters
    decree_filter = DecreeFilter(request.GET, queryset=qs)
    
    # Create the table based on the filtered queryset
    table = DecreeTable(decree_filter.qs)
    
    # Configure pagination (10 decrees per page)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    
    return render(request, 'decree_list.html', {
        'table': table,
        'filter': decree_filter,
    })
    

# Main Adding and Editing view for decrees
@login_required
def add_edit_decree(request, document_id=None):
    if document_id:
        instance = get_object_or_404(Decree, id=document_id)
    else:
        instance = None

    form = DecreeForm(request.POST or None, request.FILES or None, instance=instance)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('decree_list'))  # Adjust URL name as needed

    return render(request, 'decree_form.html', {
        'form': form,
    })


# Main PDF download view for decrees
def download_decree(request, document_id):
    """
    Downloads a decree's PDF file, attachment, or both as a ZIP file.
    """
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
    decree = get_object_or_404(Decree, pk=document_id)
    return render(request, 'decree_detail.html', {'decree': decree})


# Main table view for publications
@login_required
def publication_list(request):
    # Get the base queryset (only non-deleted items)
    qs = Publication.objects.filter(deleted_at__isnull=True)
    
    # Apply django-filters (adjust if you have a PublicationFilter)
    publication_filter = PublicationFilter(request.GET, queryset=qs)
    
    # Create the table based on the filtered queryset
    table = PublicationTable(publication_filter.qs)
    
    # Configure pagination (10 publications per page)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    
    return render(request, 'pub_list.html', {
        'table': table,
        'filter': publication_filter,
    })


# Main Adding and Editing view for publications
@login_required
def add_edit_publication(request, document_id=None):
    if document_id:
        instance = get_object_or_404(Publication, id=document_id)
    else:
        instance = None

    # If you have a form with dynamic population, you can adjust like:
    form = PublicationForm(request.POST or None, request.FILES or None, instance=instance)
    
    if request.method == 'POST' and form.is_valid():
        publication = form.save()

        # After saving, you might want to populate shared fields with the selected decree number.
        if publication.decree:
            decree = Decree.objects.filter(number=publication.decree).first()
            if decree:
                # Populate shared fields (adjust this based on actual fields)
                publication.owner = decree.company
                publication.country = decree.country
                publication.date_applied = decree.date_applied
                publication.ar_brand = decree.ar_brand
                publication.en_brand = decree.en_brand
                publication.category = decree.category
                publication.save()

        return redirect(reverse('publication_list'))  # Adjust URL name as needed

    return render(request, 'pub_form.html', {
        'form': form,
    })


# Main PDF download view for publications
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

    # Find a decree that matches the publication's decree number (if it exists)
    decree = Decree.objects.filter(number=publication.decree).first()  # Fetch the decree if it exists

    return render(request, 'pub_detail.html', {
        'publication': publication,
        'decree': decree  # Pass the decree object
    })


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
        'dec_no': pub_record.decree if pub_record.decree else "N/A",
        'applicant': pub_record.applicant if pub_record.applicant else "N/A",
        'owner': pub_record.owner if pub_record.owner else "N/A",
        'country': pub_record.get_country_display() if pub_record.country else "N/A",
        'address': pub_record.address if pub_record.address else "N/A",
        'date_applied': pub_record.date_applied.strftime("%d-%m-%Y") if pub_record.date_applied else "N/A",
        'ar_brand': pub_record.ar_brand if pub_record.ar_brand else "N/A",
        'en_brand': pub_record.en_brand if pub_record.en_brand else "N/A",
        'category': pub_record.category if pub_record.category else "N/A",
        'pub_img': pub_record.img_file.url if pub_record.img_file else "N/A",
        'e_number': pub_record.e_number if pub_record.e_number else "N/A",
        'status': pub_record.get_status_display if pub_record.status else "N/A",
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


