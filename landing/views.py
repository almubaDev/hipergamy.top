from django.shortcuts import render

def home(request):
    """
    Vista para la página de inicio (landing page) de Hipérgamia.
    """
    # No activamos idioma manualmente: lo hace LocaleMiddleware
    return render(request, 'landing/home.html')


def language_test(request):
    return render(request, 'language_test.html')
