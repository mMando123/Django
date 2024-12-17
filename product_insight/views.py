from django.http import JsonResponse
from django.utils import translation
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@require_POST
def set_language_ajax(request):
    language = request.POST.get('language', None)
    next_url = request.POST.get('next', None)
    
    if language:
        translation.activate(language)
        request.session[translation.LANGUAGE_SESSION_KEY] = language
        
        response = JsonResponse({'status': 'success', 'next': next_url})
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            language,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
        return response
    
    return JsonResponse({'status': 'error', 'message': 'Language not specified'}, status=400)
