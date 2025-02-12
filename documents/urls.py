from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main index page
    # path('manage-sections/<str:model_name>/', views.manage_sections, name='manage_sections'),

    path('decrees/', views.decree_list, name='decree_list'),

    path('decrees/add/', views.add_edit_decree, name='add_decree'),
    path('decrees/edit/<int:document_id>/', views.add_edit_decree, name='edit_decree'),
    path('decrees/detail/<int:document_id>/', views.decree_detail, name='view_decree'),
    path('decrees/download/<int:document_id>/', views.download_decree, name='download_decree'),
    path('decrees/delete/<int:document_id>/', views.soft_delete_decree, name='delete_decree'),

    path('Decree-autocomplete/', views.DecreeAutocompleteView.as_view(), name='decree-autocomplete'),

    path('publications/', views.publication_list, name='publication_list'),
    
    # Add and Edit routes for Publication
    path('publications/add/', views.add_edit_publication, name='add_publication'),
    path('publications/edit/<int:document_id>/', views.add_edit_publication, name='edit_publication'),

    # View and download routes for Publication
    path('publications/detail/<int:document_id>/', views.publication_detail, name='view_publication'),
    path('publications/download/<int:document_id>/', views.download_publication, name='download_publication'),

    # Soft delete for Publication
    path('publications/delete/<int:document_id>/', views.soft_delete_publication, name='delete_publication'),
    path('update-status/<int:publication_id>/', views.update_status, name='update_status'),
    
    path('publications/pdf/<int:pub_id>/', views.gen_pub_pdf, name='gen_pub_pdf'),

    path('formplus/', views.formplus_list, name='formplus_list'),
    path('formplus/add/', views.add_edit_formplus, name='add_formplus'),
    path('formplus/edit/<int:document_id>/', views.add_edit_formplus, name='edit_formplus'),
    path('formplus/detail/<int:document_id>/', views.formplus_detail, name='view_formplus'),
    path('formplus/download/<int:document_id>/', views.download_formplus, name='download_formplus'),
    path('formplus/delete/<int:document_id>/', views.soft_delete_formplus, name='delete_formplus'),


    # OLD Urls:
    # path('<str:model_name>/', views.document_view, name='document_view'),
    # path('add/<str:model_name>/', views.add_document, name='add_document'),
    # path('edit/<str:model_name>/<int:document_id>/', views.add_document, name='edit_document'),
    # path('decree-autocomplete/', DecreeAutocompleteView.as_view(), name='decree-autocomplete'),
    # path('download/<str:model_name>/<int:object_id>/', views.download_document, name='download_document'),
    # path('delete_document/<str:model_name>/<int:document_id>/', views.delete_document, name='delete_document'),
    # path('get_document_details/<int:document_id>/', views.get_document_details, name='get_document_details'),
]