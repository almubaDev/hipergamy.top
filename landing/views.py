from django.shortcuts import render

def home(request):
    """
    Vista para la página de inicio (landing page) de Hipérgamia.
    """
    return render(request, 'landing/home.html')

