from django.urls import path
from django.views.generic import TemplateView
from books.views import (
    upload_file,
    list_files,
    view_file,
    delete_file,
    ListFilesUploadView,
    FileDetailView,
    upload_files_s3,
    s3_file_list,
)

urlpatterns = [
    # path('upload/', upload_file, name='upload_file'),
    # path('files/', list_files, name='list_files'),
    # path('file/<int:file_id>/', view_file, name='view_file'),
    # path('file/<int:file_id>/delete/', delete_file, name='delete_file'),
    path('files_cbv/', ListFilesUploadView.as_view(), name='list_files_cbv'),
    path('file_cbv/<int:file_id>/', FileDetailView.as_view(), name='view_file_cbv'),
    path('upload_s3/', upload_files_s3, name='upload_file_s3'),
    path('files-list/', s3_file_list, name='files_s3')
]