#!/usr/bin/env python
"""
Script para diagnosticar problemas con el cambio de idiomas en Django
"""
import os
import sys
import subprocess
import requests
from urllib.parse import urljoin

def check_django_i18n_urls():
    """Verifica la configuración de las URLs para i18n"""
    print("=== Comprobando configuración de URLs de Django i18n ===")
    
    # Verificar archivo urls.py
    with open('core/urls.py', 'r', encoding='utf-8') as f:
        urls_content = f.read()
    
    # Comprobar si 'i18n/' está fuera de i18n_patterns
    if "path('i18n/', include('django.conf.urls.i18n'))" in urls_content:
        print("✓ Ruta 'i18n/' configurada correctamente")
    else:
        print("✗ Ruta 'i18n/' no encontrada o mal configurada. Debería ser:")
        print("  path('i18n/', include('django.conf.urls.i18n')),")
    
    # Comprobar si prefix_default_language está configurado
    if "prefix_default_language=False" in urls_content:
        print("✓ prefix_default_language configurado como False")
    else:
        print("⚠️ prefix_default_language no está configurado como False")
        print("  Se recomienda: prefix_default_language=False")

def check_language_settings():
    """Verifica la configuración de los ajustes de idioma"""
    print("\n=== Comprobando configuración de idiomas en settings.py ===")
    
    # Verificar archivo settings.py
    with open('core/settings.py', 'r', encoding='utf-8') as f:
        settings_content = f.read()
    
    # Comprobar LANGUAGE_CODE
    if "LANGUAGE_CODE = 'es'" in settings_content:
        print("✓ LANGUAGE_CODE configurado como 'es'")
    elif "LANGUAGE_CODE =" in settings_content:
        print(f"⚠️ LANGUAGE_CODE no está configurado como 'es'")
    else:
        print("✗ LANGUAGE_CODE no encontrado")
    
    # Comprobar USE_I18N
    if "USE_I18N = True" in settings_content:
        print("✓ USE_I18N configurado como True")
    else:
        print("✗ USE_I18N no encontrado o no configurado como True")
    
    # Comprobar LANGUAGES
    if "LANGUAGES = [" in settings_content and "('es', _('Español'))" in settings_content and "('en', _('English'))" in settings_content:
        print("✓ LANGUAGES configurado correctamente con 'es' y 'en'")
    else:
        print("⚠️ LANGUAGES puede no estar configurado correctamente")
    
    # Comprobar LOCALE_PATHS
    if "LOCALE_PATHS = [" in settings_content and "os.path.join(BASE_DIR, 'locale')" in settings_content:
        print("✓ LOCALE_PATHS configurado correctamente")
    else:
        print("✗ LOCALE_PATHS no encontrado o mal configurado")
    
    # Comprobar LocaleMiddleware
    if "'django.middleware.locale.LocaleMiddleware'" in settings_content:
        print("✓ LocaleMiddleware presente en MIDDLEWARE")
    else:
        print("✗ LocaleMiddleware no encontrado en MIDDLEWARE")

def check_mo_files():
    """Verifica que los archivos .mo estén presentes y tengan el tamaño adecuado"""
    print("\n=== Comprobando archivos .mo ===")
    
    for lang in ['es', 'en']:
        mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'
        if os.path.exists(mo_path):
            size = os.path.getsize(mo_path)
            print(f"✓ {mo_path} existe ({size} bytes)")
        else:
            print(f"✗ {mo_path} no existe")

def check_template():
    """Verifica la plantilla de navbar.html"""
    print("\n=== Comprobando plantilla navbar.html ===")
    
    # Verificar archivo navbar.html
    with open('templates/partials/navbar.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Comprobar carga de i18n
    if "{% load i18n %}" in template_content:
        print("✓ Carga de i18n presente")
    else:
        print("✗ Falta {% load i18n %}")
    
    # Comprobar formulario para español
    if '<form action="{% url \'set_language\' %}" method="post"' in template_content and '<input type="hidden" name="language" value="es">' in template_content:
        print("✓ Formulario para español configurado correctamente")
    else:
        print("⚠️ Formulario para español puede tener problemas")
    
    # Comprobar formulario para inglés
    if '<form action="{% url \'set_language\' %}" method="post"' in template_content and '<input type="hidden" name="language" value="en">' in template_content:
        print("✓ Formulario para inglés configurado correctamente")
    else:
        print("⚠️ Formulario para inglés puede tener problemas")
    
    # Comprobar campo next
    if 'value="{{ request.get_full_path }}"' in template_content:
        print("✓ Campo next usa request.get_full_path")
    elif 'value="{{ request.path }}"' in template_content:
        print("✗ Campo next usa request.path en lugar de request.get_full_path")
    else:
        print("⚠️ No se encontró configuración para el campo next")

def main():
    """Función principal"""
    print("=" * 60)
    print("DIAGNÓSTICO DE PROBLEMAS DE CAMBIO DE IDIOMA EN DJANGO")
    print("=" * 60)
    
    check_django_i18n_urls()
    check_language_settings()
    check_mo_files()
    check_template()
    
    print("\n" + "=" * 60)
    print("RECOMENDACIONES:")
    print("1. Asegúrate de usar 'request.get_full_path' en el campo 'next'")
    print("2. Verifica que los formularios envíen a 'set_language'")
    print("3. Comprueba que el valor de 'language' sea correcto")
    print("4. Reinicia el servidor Django después de realizar cambios")
    print("=" * 60)

if __name__ == "__main__":
    main()
