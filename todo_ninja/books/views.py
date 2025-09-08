import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from books.models import UploadedFiles
from books.signals import file_word_count
from books.redis_client import RedisClient


def upload_file(request):
    redis_client = RedisClient()

    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        if not file.name.endswith('.txt'):
            return JsonResponse({'error': 'Invalid file type, only .txt allowed'}, status=400)
        try:
            content = file.read().decode('utf-8')
            word_count = len(content.split())
            char_count = len(content)

            uploaded_file = UploadedFiles.objects.create(
                file=file,
                filename=file.name,
                word_count=word_count,
                char_count=char_count
            )
            breakpoint()
            redis_client.set_data(
                uploaded_file.pk,
                {'id':uploaded_file.pk, 'filename': file.name, 'file_url': uploaded_file.file.url},
                expire=3600
            )
            file_word_count.send(
                sender=UploadedFiles,
                instance=uploaded_file,
                word_limit=3
            )

            return JsonResponse({
                'id': uploaded_file.id,
                'filename': file.name,
                'word_count': word_count,
                'char_count':char_count,
                'upladed_at': uploaded_file.upladed_at.strftime('%Y-%m-%d %H:%M:%S'),
                'file_url': uploaded_file.file.url
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'No file provided'}, status=400)

def list_files(request):
    redis_client = RedisClient()
    files = UploadedFiles.objects.all().order_by('-upladed_at')
    file_list = [{
        'id': f.id,
        'filename': f.filename,
        'word_count': f.word_count,
        'char_count':f.char_count,
        'upladed_at': f.upladed_at.strftime('%Y-%m-%d %H:%M:%S'),
        'file_url': f.file.url
    } for f in files]
    redis_file_list = [redis_client.get_data(f.pk) for f in files]
    return JsonResponse({'files': file_list, 'redis_files': redis_file_list})

def view_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFiles, id=file_id)
    try:
        with uploaded_file.file.open('r') as f:
            content = f.read()
        return JsonResponse({
                'id': uploaded_file.id,
                'filename': uploaded_file.filename,
                'content': content,
                'word_count':uploaded_file.word_count,
                'char_count':uploaded_file.char_count,
                'upladed_at': uploaded_file.upladed_at.strftime('%Y-%m-%d %H:%M:%S'),
                'file_url': uploaded_file.file.url
            })
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    

def delete_file(request, file_id):
    if request.method == 'POST':
        uploaded_file = get_object_or_404(UploadedFiles, id=file_id)
        try:
            uploaded_file.delete()
            return JsonResponse({'message': 'File deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=500)


class ListFilesUploadView(View):
    redis_client = RedisClient()
    def get(self, request):
        files = UploadedFiles.objects.all().order_by('-upladed_at')
        file_list = [{
            'id': f.id,
            'filename': f.filename,
            'word_count': f.word_count,
            'char_count':f.char_count,
            'upladed_at': f.upladed_at.strftime('%Y-%m-%d %H:%M:%S'),
            'file_url': f.file.url
        } for f in files]
        redis_file_list = [self.redis_client.get_data(f.pk) for f in files if self.redis_client.get_data(f.pk)]
        return JsonResponse({'files': file_list, 'redis_files': redis_file_list})
    
    def post(self, request):
        if request.FILES.get('file'):
            file = request.FILES['file']
            if not file.name.endswith('.txt'):
                return JsonResponse({'error': 'Invalid file type, only .txt allowed'}, status=400)
            try:
                content = file.read().decode('utf-8')
                word_count = len(content.split())
                char_count = len(content)

                uploaded_file = UploadedFiles.objects.create(
                    file=file,
                    filename=file.name,
                    word_count=word_count,
                    char_count=char_count
                )
                self.redis_client.set_data(
                    uploaded_file.pk,
                    {'id':uploaded_file.pk, 'filename': file.name, 'file_url': uploaded_file.file.url},
                    expire=40
                )
                file_word_count.send(
                    sender=UploadedFiles,
                    instance=uploaded_file,
                    word_limit=3
                )
                return JsonResponse({
                    'id': uploaded_file.id,
                    'filename': file.name,
                    'word_count': word_count,
                    'char_count':char_count,
                    'upladed_at': uploaded_file.upladed_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'file_url': uploaded_file.file.url
                })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'error': 'No file provided'}, status=400)


class FileDetailView(View):
    def get(self, request, file_id):
        uploaded_file = get_object_or_404(UploadedFiles, id=file_id)
        try:
            with uploaded_file.file.open('r') as f:
                content = f.read()
            return JsonResponse({
                    'id': uploaded_file.id,
                    'filename': uploaded_file.filename,
                    'content': content,
                    'word_count':uploaded_file.word_count,
                    'char_count':uploaded_file.char_count,
                    'upladed_at': uploaded_file.upladed_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'file_url': uploaded_file.file.url
                })
        except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, file_id):
        uploaded_file = get_object_or_404(UploadedFiles, id=file_id)
        try:
            uploaded_file.delete()
            return JsonResponse({'message': 'File deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
# class DeleteFileView(View):
#     def delete(self, request, file_id):
#         uploaded_file = get_object_or_404(UploadedFiles, id=file_id)
#         try:
#             uploaded_file.delete()
#             return JsonResponse({'message': 'File deleted successfully'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

def upload_files_s3(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        default_storage.save(file.name, ContentFile(file.read()))
    return redirect('files_s3')