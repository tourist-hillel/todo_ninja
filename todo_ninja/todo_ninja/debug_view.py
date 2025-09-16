
from django.http import HttpResponse

def debug_session(request):
    language = request.session.get('django_language', 'Не встановлено')
    current_language = request.LANGUAGE_CODE
    return HttpResponse(f"Мова в сесії: {language}<br>Поточна мова: {current_language}")