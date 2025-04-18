# Guarda este script como check_mo_files.py
import os

def check_mo_file(path):
    """Verifica si un archivo .mo existe y tiene contenido."""
    if os.path.exists(path):
        size = os.path.getsize(path)
        if size > 0:
            return f"✅ El archivo existe y tiene {size} bytes"
        else:
            return "❌ El archivo existe pero está vacío (0 bytes)"
    else:
        return "❌ El archivo no existe"

# Verifica los archivos .mo para inglés y español
en_mo_path = os.path.join('locale', 'en', 'LC_MESSAGES', 'django.mo')
es_mo_path = os.path.join('locale', 'es', 'LC_MESSAGES', 'django.mo')

print("Archivo .mo en inglés:", check_mo_file(en_mo_path))
print("Archivo .mo en español:", check_mo_file(es_mo_path))