"""
Script para crear archivos .po limpios para solucionar el problema de cambio de idioma
"""
import os

def write_spanish_po_file():
    """Escribe un archivo .po limpio para español"""
    content = """# Translation for Hypergamy.
# Copyright (C) 2025 Hypergamy Team
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
"""
    
    # Asegurarse de que el directorio existe
    os.makedirs('locale/es/LC_MESSAGES', exist_ok=True)
    
    with open('locale/es/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Archivo español django.po creado correctamente")

def write_english_po_file():
    """Escribe un archivo .po limpio para inglés"""
    content = """# Translation for Hypergamy.
# Copyright (C) 2025 Hypergamy Team
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
"""
    
    # Asegurarse de que el directorio existe
    os.makedirs('locale/en/LC_MESSAGES', exist_ok=True)
    
    with open('locale/en/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Archivo inglés django.po creado correctamente")

if __name__ == "__main__":
    print("Creando archivos .po limpios...")
    write_spanish_po_file()
    write_english_po_file()
    print("\nAhora ejecuta este comando para compilar los archivos .mo:")
    print("msgfmt -o locale/es/LC_MESSAGES/django.mo locale/es/LC_MESSAGES/django.po")
    print("msgfmt -o locale/en/LC_MESSAGES/django.mo locale/en/LC_MESSAGES/django.po")
