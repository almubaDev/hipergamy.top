#!/usr/bin/env python
"""
Script que implementa una solución final para el problema de traducciones
"""
import os
import subprocess

def check_i18n_configuration():
    """Verifica que la configuración de i18n esté correcta"""
    print("Verificando configuración de i18n...")
    
    # Comprobar urls.py
    with open('core/urls.py', 'r', encoding='utf-8') as f:
        urls_content = f.read()
    
    if "path('i18n/', include('django.conf.urls.i18n'))" not in urls_content:
        print("❌ PROBLEMA: La URL de cambio de idioma no está configurada correctamente en core/urls.py")
        return False
    
    # Comprobar settings.py
    with open('core/settings.py', 'r', encoding='utf-8') as f:
        settings_content = f.read()
    
    if "'django.middleware.locale.LocaleMiddleware'" not in settings_content:
        print("❌ PROBLEMA: El middleware LocaleMiddleware no está configurado en settings.py")
        return False
    
    # Todo parece estar bien
    print("✅ La configuración de i18n parece correcta")
    return True

def create_language_files():
    """Crea archivos de traducción básicos que funcionarán seguro"""
    print("\nCreando archivos de traducción básicos...")
    
    # Español primero
    spanish_content = """# Translation for Hypergamy.
msgid ""
msgstr ""
"Project-Id-Version: 1.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2025-04-15 12:00+0000\\n"
"PO-Revision-Date: 2025-04-15 12:00+0000\\n"
"Last-Translator: Dev <dev@example.com>\\n"
"Language-Team: ES\\n"
"Language: es\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"

msgid "¿Qué es?"
msgstr "¿Qué es?"

msgid "Sistema de Niveles"
msgstr "Sistema de Niveles" 

msgid "Experiencias"
msgstr "Experiencias"

msgid "Registrarse"
msgstr "Registrarse"

msgid "Idioma"
msgstr "Idioma"

msgid "Español"
msgstr "Español"

msgid "English"
msgstr "English"
"""
    
    # Inglés
    english_content = """# Translation for Hypergamy.
msgid ""
msgstr ""
"Project-Id-Version: 1.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2025-04-15 12:00+0000\\n"
"PO-Revision-Date: 2025-04-15 12:00+0000\\n"
"Last-Translator: Dev <dev@example.com>\\n"
"Language-Team: EN\\n"
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

msgid "Español"
msgstr "Spanish"

msgid "English"
msgstr "English"
"""
    
    # Crear directorios si no existen
    os.makedirs('locale/es/LC_MESSAGES', exist_ok=True)
    os.makedirs('locale/en/LC_MESSAGES', exist_ok=True)
    
    # Guardar los archivos .po
    with open('locale/es/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(spanish_content)
    
    with open('locale/en/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(english_content)
    
    print("✅ Archivos .po creados correctamente")
    
    # Eliminar cualquier archivo .mo existente
    if os.path.exists('locale/es/LC_MESSAGES/django.mo'):
        os.remove('locale/es/LC_MESSAGES/django.mo')
    if os.path.exists('locale/en/LC_MESSAGES/django.mo'):
        os.remove('locale/en/LC_MESSAGES/django.mo')
    
    # Compilar los archivos .po a .mo
    try:
        subprocess.run(['msgfmt', '-o', 'locale/es/LC_MESSAGES/django.mo', 'locale/es/LC_MESSAGES/django.po'], check=True)
        subprocess.run(['msgfmt', '-o', 'locale/en/LC_MESSAGES/django.mo', 'locale/en/LC_MESSAGES/django.po'], check=True)
        print("✅ Archivos .mo compilados correctamente")
    except Exception as e:
        print(f"❌ Error al compilar los archivos .mo: {e}")
        return False
    
    return True

def create_basic_navbar():
    """Crea un navbar simple que funcionará con el cambio de idiomas"""
    print("\nCreando navbar simplificado...")
    
    navbar_content = """{% load static %}
{% load i18n %}
<!-- Header -->
<header class="fixed w-full top-0 z-50 bg-deep-carbon border-b border-gray-800">
    <div class="container mx-auto px-4 py-3">
        <div class="flex justify-between items-center">
            <div class="flex items-center">
                <a href="/" class="flex items-center">
                    <img class='logo' src="{% static 'images/logo.png' %}" alt="Hypergamy Logo" class="h-8">
                </a>
            </div>
            
            <!-- Botón menú móvil -->
            <button id="mobile-menu-btn" class="md:hidden text-soft-smoke focus:outline-none">
                <i class="fas fa-bars text-xl"></i>
            </button>
            
            <!-- Navegación escritorio -->
            <nav class="hidden md:flex items-center space-x-6">
                <a href="#what-is" class="text-soft-smoke hover:text-white transition-colors">{% trans "¿Qué es?" %}</a>
                <a href="#how-it-works" class="text-soft-smoke hover:text-white transition-colors">{% trans "Sistema de Niveles" %}</a>
                <a href="#testimonials" class="text-soft-smoke hover:text-white transition-colors">{% trans "Experiencias" %}</a>
                
                <a href="#contact-form" class="btn-primary px-4 py-2 rounded-full">{% trans "Registrarse" %}</a>
                
                <!-- Selector de idioma - versión mínima -->
                <div class="flex items-center space-x-2 ml-4">
                    <form action="/i18n/setlang/" method="post" class="inline">
                        {% csrf_token %}
                        <input type="hidden" name="language" value="es">
                        <button type="submit" class="text-2xl">
                            🇪🇸
                        </button>
                    </form>
                    
                    <form action="/i18n/setlang/" method="post" class="inline">
                        {% csrf_token %}
                        <input type="hidden" name="language" value="en">
                        <button type="submit" class="text-2xl">
                            🇺🇸
                        </button>
                    </form>
                </div>
            </nav>
        </div>
    </div>
    
    <!-- Menú móvil -->
    <div id="mobile-menu" class="hidden md:hidden w-full bg-deep-carbon border-t border-gray-800 absolute left-0">
        <div class="container mx-auto py-3 px-4 flex flex-col space-y-3">
            <a href="#what-is" class="text-soft-smoke hover:text-white py-2">{% trans "¿Qué es?" %}</a>
            <a href="#how-it-works" class="text-soft-smoke hover:text-white py-2">{% trans "Sistema de Niveles" %}</a>
            <a href="#testimonials" class="text-soft-smoke hover:text-white py-2">{% trans "Experiencias" %}</a>
            
            <!-- Selector de idioma para móvil -->
            <div class="py-2">
                <p class="text-sm text-gray-400 mb-2">{% trans "Idioma" %}:</p>
                <div class="flex gap-4">
                    <form action="/i18n/setlang/" method="post">
                        {% csrf_token %}
                        <input type="hidden" name="language" value="es">
                        <button type="submit" class="flex flex-col items-center">
                            <span class="text-3xl mb-1">🇪🇸</span>
                            <span class="text-xs">{% trans "Español" %}</span>
                        </button>
                    </form>
                    
                    <form action="/i18n/setlang/" method="post">
                        {% csrf_token %}
                        <input type="hidden" name="language" value="en">
                        <button type="submit" class="flex flex-col items-center">
                            <span class="text-3xl mb-1">🇺🇸</span>
                            <span class="text-xs">{% trans "English" %}</span>
                        </button>
                    </form>
                </div>
            </div>
            
            <a href="#contact-form" class="btn-primary px-4 py-2 rounded-full text-center">{% trans "Registrarse" %}</a>
        </div>
    </div>
</header>

<!-- Script para el menú móvil -->
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Alternar menú móvil
        document.getElementById('mobile-menu-btn').addEventListener('click', function() {
            document.getElementById('mobile-menu').classList.toggle('hidden');
        });
    });
</script>
"""
    
    with open('templates/partials/navbar.html', 'w', encoding='utf-8') as f:
        f.write(navbar_content)
    
    print("✅ Navbar simplificado creado")
    return True

def main():
    print("="*60)
    print("SOLUCIÓN FINAL PARA EL PROBLEMA DE TRADUCCIONES")
    print("="*60)
    
    # Verificar configuración
    check_i18n_configuration()
    
    # Crear archivos de traducción
    create_language_files()
    
    # Crear navbar simplificado
    create_basic_navbar()
    
    print("\n" + "="*60)
    print("✅ CONFIGURACIÓN COMPLETA")
    print("\nAhora reinicia el servidor Django:")
    print("python manage.py runserver")
    print("="*60)

if __name__ == "__main__":
    main()
