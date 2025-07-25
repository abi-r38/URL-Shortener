# shortener/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
import json
import random
import string
from .models import URL
from django.views.decorators.csrf import csrf_exempt

def home_view(request):
    """ This view just displays the main HTML page. """
    return render(request, 'index.html')

@csrf_exempt
def create_short_url(request):
    if request.method != 'POST':

        def create_short_url(request):
            """ This view handles API requests to create new short URLs. """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
    try:
        data = json.loads(request.body)
        long_url = data.get('long_url')

        if not long_url:
            return JsonResponse({'error': 'URL field is required.'}, status=400)
        
        # Algorithm to generate a unique 6-character short code.
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choices(characters, k=6))
            if not URL.objects.filter(pk=short_code).exists():
                break # Break the loop once we find a unique code

        # Save the new object to the PostgreSQL database.
        # Django's ORM converts this into an SQL 'INSERT' command.
        URL.objects.create(short_code=short_code, long_url=long_url)

        # Build the full URL to return to the user.
        full_short_url = request.build_absolute_uri(f'/{short_code}')

        return JsonResponse({'short_url': full_short_url})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

def redirect_view(request, short_code):
    """
    Finds the long URL from the database and redirects the user.
    """
    # get_object_or_404 is a handy shortcut from Django. It runs an
    # SQL 'SELECT' query. If it finds nothing, it automatically returns a 404 page.
    url_mapping = get_object_or_404(URL, pk=short_code)
    
    # This response tells the browser "Don't stay here, go to this other address instead."
    return HttpResponseRedirect(url_mapping.long_url)