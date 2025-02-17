from django.urls import path
from . import views

urlpatterns = [
    # Main index View
    path('', views.index, name='index'),
    
    # Manage-Sections Complete View
    path('manage/sections/', views.core_models_view, name='manage_sections'),
    
    # Main View Table for Decree model
    path('decrees/', views.decree_list, name='decree_list'),
    
    # CRUD routes for Decree model
    path('decrees/add/', views.add_edit_decree, name='add_decree'),
    path('decrees/edit/<int:document_id>/', views.add_edit_decree, name='edit_decree'),
    path('decrees/detail/<int:document_id>/', views.decree_detail, name='view_decree'),
    path('decrees/download/<int:document_id>/', views.download_decree, name='download_decree'),
    path('decrees/delete/<int:document_id>/', views.soft_delete_decree, name='delete_decree'),
    
    # AJAX autocomplete function for Publication model
    path('decree-autocomplete/', views.DecreeAutocompleteView.as_view(), name='decree-autocomplete'),
    
    # Main View Table for Publication model
    path('publications/', views.publication_list, name='publication_list'),
    
    # CRUD routes for Publication model
    path('publications/add/', views.add_edit_publication, name='add_publication'),
    path('publications/edit/<int:document_id>/', views.add_edit_publication, name='edit_publication'),
    path('publications/detail/<int:document_id>/', views.publication_detail, name='view_publication'),
    path('publications/download/<int:document_id>/', views.download_publication, name='download_publication'),
    path('publications/delete/<int:document_id>/', views.soft_delete_publication, name='delete_publication'),
    
    # AJAX Mark Complete function for Publication model
    path('update-status/<int:publication_id>/', views.update_status, name='update_status'),
    
    # PDF generation for Publication model initial
    path('publications/pdf/<int:pub_id>/', views.gen_pub_pdf, name='gen-pub-pdf'),
    
    # PDF generation for Publication model final
    # path('publications/pdf_f/<int:pub_id>/', views.gen_pub_pdf, name='gen_pub_pdf_f'),
    
    # AJAX autocomplete function for Objection model
    path('publication-autocomplete/', views.PublicationAutocompleteView.as_view(), name='pub-autocomplete'),
    
    # Main View Table for Objection model
    path('objections/', views.objection_list, name='objection_list'),
    
    # CRUD routes for Publication model
    path('objections/add/', views.add_edit_objection, name='add_objection'),
    path('objections/edit/<int:document_id>/', views.add_edit_objection, name='edit_objection'),
    path('objections/detail/<int:document_id>/', views.objection_detail, name='view_objection'),
    path('objections/download/<int:document_id>/', views.download_objection, name='download_objection'),
    path('objections/delete/<int:document_id>/', views.soft_delete_objection, name='delete_objection'),
    
    # PDF generation for Objection model
    # path('objections/pdf/<int:pub_id>/', views.gen_obj_pdf, name='gen_obj_pdf'),
    
    # Main View Table for FormPlus model
    path('formplus/', views.formplus_list, name='formplus_list'),
    
    # CRUD routes for FormPlus model
    path('formplus/add/', views.add_edit_formplus, name='add_formplus'),
    path('formplus/edit/<int:document_id>/', views.add_edit_formplus, name='edit_formplus'),
    path('formplus/detail/<int:document_id>/', views.formplus_detail, name='view_formplus'),
    path('formplus/download/<int:document_id>/', views.download_formplus, name='download_formplus'),
    path('formplus/delete/<int:document_id>/', views.soft_delete_formplus, name='delete_formplus'),
]