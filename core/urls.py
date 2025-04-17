from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# URLs que no necesitan ser traducidas
urlpatterns = [
    # URLs para cambiar idioma
    path('i18n/', include('django.conf.urls.i18n')),
]

# URLs que se traducirán según el idioma
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    #path('app/', include('application.urls')),
    # Si prefieres URLs sin prefijo para el idioma por defecto, agrega:
    prefix_default_language=False
)

# Configuración para servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)