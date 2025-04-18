from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL necesaria para el formulario de cambio de idioma
    path('i18n/', include('django.conf.urls.i18n')),

    # Admin y rutas de la app principal
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    # path('app/', include('application.urls')),  # si lo necesitas más adelante
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
