from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView

# URLs sin traducción
urlpatterns = [
    # Redirección desde la raíz a español
    path('', RedirectView.as_view(url='/es/'), name='root'),
    path('i18n/', include('django.conf.urls.i18n')),
]

# URLs con patrones de internacionalización
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    # Prefijo obligatorio para todos los idiomas
    prefix_default_language=True
)

# Archivos estáticos
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)