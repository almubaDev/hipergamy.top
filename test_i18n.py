import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils import translation

# Texto a traducir
test_text = "¿Qué es?"

# Probar con inglés
translation.activate('en')
print(f"Idioma actual: {translation.get_language()}")
from django.utils.translation import gettext as _
print(f"'{test_text}' traducido a inglés: '{_(test_text)}'")

# Probar con español
translation.activate('es')
print(f"Idioma actual: {translation.get_language()}")
print(f"'{test_text}' traducido a español: '{_(test_text)}'")