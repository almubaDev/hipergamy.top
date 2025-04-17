#!/usr/bin/env python
"""
Script que soluciona el problema de cambio de idioma de manera directa
"""
import os
import shutil
import subprocess

def clean_translation_files():
    """Elimina todos los archivos de traducción existentes"""
    print("Limpiando archivos de traducción existentes...")
    
    # Eliminar archivos .mo
    for lang in ['es', 'en']:
        mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'
        if os.path.exists(mo_path):
            try:
                os.remove(mo_path)
                print(f"  ✓ Eliminado {mo_path}")
            except Exception as e:
                print(f"  ✗ No se pudo eliminar {mo_path}: {e}")
    
    # Limpiar archivos .po
    for lang in ['es', 'en']:
        po_path = f'locale/{lang}/LC_MESSAGES/django.po'
        if os.path.exists(po_path):
            # Hacer backup si no existe ya
            backup = f"{po_path}.ultimo_backup"
            if not os.path.exists(backup):
                shutil.copy2(po_path, backup)
                print(f"  ✓ Backup creado: {backup}")

def create_minimal_po_files():
    """Crea archivos .po mínimos pero correctos"""
    print("\nCreando archivos .po mínimos...")

    # Español
    es_content = """# Translation for Hypergamy
msgid ""
msgstr ""
"Project-Id-Version: 1.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2025-04-17 00:00-0400\\n"
"PO-Revision-Date: 2025-04-17 00:00-0400\\n"
"Last-Translator: DEV\\n"
"Language: es\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"

msgid "What is it?"
msgstr "¿Qué es?"

msgid "Level System"
msgstr "Sistema de Niveles"

msgid "Experiences"
msgstr "Experiencias"

msgid "Sign up"
msgstr "Registrarse"

msgid "Language"
msgstr "Idioma"

msgid "English"
msgstr "Inglés"

msgid "Spanish"
msgstr "Español"
"""
    # Inglés
    en_content = """# Translation for Hypergamy
msgid ""
msgstr ""
"Project-Id-Version: 1.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2025-04-17 00:00-0400\\n"
"PO-Revision-Date: 2025-04-17 00:00-0400\\n"
"Last-Translator: DEV\\n"
"Language: en\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"

msgid "¿Qué es?"
msgstr "What is it?"

msgid "Sistema de Niveles"
msgstr "Level System"

msgid "Experiencias"
msgstr "Experiences"

msgid "Registrarse"
msgstr "Sign up"

msgid "Idioma"
msgstr "Language"

msgid "Inglés"
msgstr "English"

msgid "Español"
msgstr "Spanish"
"""
    
    # Asegurar que los directorios existen
    os.makedirs('locale/es/LC_MESSAGES', exist_ok=True)
    os.makedirs('locale/en/LC_MESSAGES', exist_ok=True)
    
    # Guardar archivos
    with open('locale/es/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(es_content)
    print("  ✓ Creado archivo django.po para español")
    
    with open('locale/en/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(en_content)
    print("  ✓ Creado archivo django.po para inglés")

def compile_po_files():
    """Compila los archivos .po a .mo"""
    print("\nCompilando archivos .po a .mo...")
    
    # Compilar español
    try:
        subprocess.run(['msgfmt', '-o', 'locale/es/LC_MESSAGES/django.mo', 'locale/es/LC_MESSAGES/django.po'], 
                      check=True, capture_output=True)
        print("  ✓ Compilado django.mo para español")
    except Exception as e:
        print(f"  ✗ Error compilando español: {e}")
    
    # Compilar inglés
    try:
        subprocess.run(['msgfmt', '-o', 'locale/en/LC_MESSAGES/django.mo', 'locale/en/LC_MESSAGES/django.po'], 
                      check=True, capture_output=True)
        print("  ✓ Compilado django.mo para inglés")
    except Exception as e:
        print(f"  ✗ Error compilando inglés: {e}")

def fix_navbar():
    """Crea un navbar con enlaces directos absolutamente simples"""
    print("\nCreando navbar ultra simplificado...")
    
    navbar_content = """{% load static %}
{% load i18n %}
<!-- Header ultra-simple -->
<header class="fixed w-full top-0 z-50 bg-deep-carbon border-b border-gray-800">
    <div class="container mx-auto px-4 py-3">
        <div class="flex justify-between items-center">
            <!-- Logo -->
            <div class="flex items-center">
                <a href="/" class="flex items-center">
                    <img class='logo' src="{% static 'images/logo.png' %}" alt="Hypergamy Logo" class="h-8">
                </a>
            </div>
            
            <!-- Menú móvil -->
            <button id="mobile-menu-btn" class="md:hidden text-soft-smoke focus:outline-none">
                <i class="fas fa-bars text-xl"></i>
            </button>
            
            <!-- Menú escritorio -->
            <nav class="hidden md:flex items-center space-x-6">
                <a href="#what-is" class="text-soft-smoke hover:text-white transition-colors">
                    {% if LANGUAGE_CODE == 'es' %}¿Qué es?{% else %}What is it?{% endif %}
                </a>
                <a href="#how-it-works" class="text-soft-smoke hover:text-white transition-colors">
                    {% if LANGUAGE_CODE == 'es' %}Sistema de Niveles{% else %}Level System{% endif %}
                </a>
                <a href="#testimonials" class="text-soft-smoke hover:text-white transition-colors">
                    {% if LANGUAGE_CODE == 'es' %}Experiencias{% else %}Experiences{% endif %}
                </a>
                
                <a href="#contact-form" class="btn-primary px-4 py-2 rounded-full">
                    {% if LANGUAGE_CODE == 'es' %}Registrarse{% else %}Sign up{% endif %}
                </a>
                
                <!-- Enlaces idioma simplificados al máximo -->
                <div class="ml-4 flex items-center space-x-4">
                    <a href="/" class="block text-2xl hover:opacity-100 {% if LANGUAGE_CODE == 'es' %}opacity-100 border-b-2 border-gold-royal{% else %}opacity-50{% endif %}">
                        🇪🇸
                    </a>
                    <a href="/en/" class="block text-2xl hover:opacity-100 {% if LANGUAGE_CODE == 'en' %}opacity-100 border-b-2 border-gold-royal{% else %}opacity-50{% endif %}">
                        🇺🇸
                    </a>
                </div>
            </nav>
        </div>
    </div>
    
    <!-- Menú móvil -->
    <div id="mobile-menu" class="hidden md:hidden w-full bg-deep-carbon border-t border-gray-800 absolute left-0">
        <div class="container mx-auto py-3 px-4 flex flex-col space-y-3">
            <a href="#what-is" class="text-soft-smoke hover:text-white py-2">
                {% if LANGUAGE_CODE == 'es' %}¿Qué es?{% else %}What is it?{% endif %}
            </a>
            <a href="#how-it-works" class="text-soft-smoke hover:text-white py-2">
                {% if LANGUAGE_CODE == 'es' %}Sistema de Niveles{% else %}Level System{% endif %}
            </a>
            <a href="#testimonials" class="text-soft-smoke hover:text-white py-2">
                {% if LANGUAGE_CODE == 'es' %}Experiencias{% else %}Experiences{% endif %}
            </a>
            
            <!-- Idiomas móvil -->
            <div class="py-2">
                <p class="text-sm text-gray-400 mb-2">
                    {% if LANGUAGE_CODE == 'es' %}Idioma{% else %}Language{% endif %}:
                </p>
                <div class="flex gap-4">
                    <a href="/" class="block flex flex-col items-center">
                        <span class="text-3xl mb-1">🇪🇸</span>
                        <span class="text-xs {% if LANGUAGE_CODE == 'es' %}text-gold-royal font-medium{% else %}text-gray-300{% endif %}">
                            {% if LANGUAGE_CODE == 'es' %}Español{% else %}Spanish{% endif %}
                        </span>
                    </a>
                    <a href="/en/" class="block flex flex-col items-center">
                        <span class="text-3xl mb-1">🇺🇸</span>
                        <span class="text-xs {% if LANGUAGE_CODE == 'en' %}text-gold-royal font-medium{% else %}text-gray-300{% endif %}">
                            {% if LANGUAGE_CODE == 'es' %}Inglés{% else %}English{% endif %}
                        </span>
                    </a>
                </div>
            </div>
            
            <a href="#contact-form" class="btn-primary px-4 py-2 rounded-full text-center">
                {% if LANGUAGE_CODE == 'es' %}Registrarse{% else %}Sign up{% endif %}
            </a>
        </div>
    </div>
</header>

<!-- Script para el menú móvil -->
<script>
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('mobile-menu-btn').addEventListener('click', function() {
            document.getElementById('mobile-menu').classList.toggle('hidden');
        });
    });
</script>
"""
    
    # Crear backup
    if os.path.exists('templates/partials/navbar.html'):
        shutil.copy2('templates/partials/navbar.html', 'templates/partials/navbar.html.backup')
        print("  ✓ Backup creado para navbar.html")
    
    # Guardar nuevo navbar
    with open('templates/partials/navbar.html', 'w', encoding='utf-8') as f:
        f.write(navbar_content)
    print("  ✓ Creado navbar ultra simplificado")

def main():
    print("="*70)
    print("SOLUCIÓN DEFINITIVA PARA EL PROBLEMA DE CAMBIO DE IDIOMAS")
    print("="*70)
    
    clean_translation_files()
    create_minimal_po_files()
    compile_po_files()
    fix_navbar()
    
    print("\n" + "="*70)
    print("SOLUCIÓN COMPLETADA")
    print("\nDEBERÍA FUNCIONAR AHORA. PASOS FINALES:")
    print("1. Reinicia completamente el servidor Django: Ctrl+C y luego python manage.py runserver")
    print("2. En el navegador, asegúrate de borrar la caché o usar modo incógnito")
    print("3. Prueba los enlaces de cambio de idioma")
    print("="*70)

if __name__ == "__main__":
    main()
